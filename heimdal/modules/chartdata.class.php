<?php
class ChartData {
    var $asset_pair;

    function __construct($asset_pair, $subsystem='odin') {
        $this->asset_pair = $asset_pair;
        $this->asset_pair['odin']['chart']['labels'] = $this->labels($asset_pair);
        $this->asset_pair['odin']['chart']['trades'] = $this->trades($asset_pair);
        $this->asset_pair['odin']['chart']['decisions'] = $this->decisions($asset_pair);
        $this->asset_pair['odin']['chart']['actions'] = $this->actions($asset_pair);
        $this->asset_pair['odin']['chart']['analyses'] = $this->analyses($asset_pair);

        //print_r($this->asset_pair['odin']['chart']['actions']);
    }

    private function datetime($time) {
         return date('Y-m-d H:i:s',$time);
    }

    function labels($asset_pair) {
        $trades_p = [];
        $trades_s = [];
        if (isset($asset_pair['odin']['trades']['list'])) {
            foreach($asset_pair['odin']['trades']['list'] as $trade) {
                if ($trade['direction'] == "s") {
                    $trades_s[] = $trade;
                }
                else {
                    $trades_p[] = $trade;
                }
            }
        }
        $len_trades_p = count($trades_p);
        $len_trades_s = count($trades_s);

        if ($len_trades_p > 0) {
            $start_ts = $trades_p[0]['time'];
            $end_ts = $trades_p[$len_trades_p - 1]['time'];

            if ($len_trades_s > 0) {
                if ($trades_s[0]['time'] < $start_ts) {
                    $start_ts = $trades_s[0]['time'];
                }
                if ($trades_s[$len_trades_s - 1]['time'] > $end_ts) {
                    $end_ts = $trades_s[$len_trades_s - 1]['time'];
                }
            }
        }
        else if ($len_trades_s > 0) {
            $start_ts = $trades_s[0]['time'];
            $end_ts = $trades_s[$len_trades_s - 1]['time'];
        }
        $labels = array();
        if (isset($start_ts) && isset($end_ts)) {
            $d_start = date('Y-m-d H:i',$start_ts);
            $d_end = date('Y-m-d H:i',$end_ts + 60);
            $start_ts = strtotime($d_start);
            $end_ts = strtotime($d_end);
            $less = true;
            while($less == true) {
                $labels[] = date('Y-m-d H:i', $start_ts);
                $start_ts += 60;
                if ($start_ts > $end_ts) { break; }
            }
        }

        return $labels;
    }

    function trades($asset_pair) {
        $t['purchases'] = [];
        $t['sales'] = [];

        if (isset($asset_pair['odin']['trades']['list'])) {
            foreach($this->asset_pair['odin']['trades']['list'] as $trade) {
                $trade['time'] = $this->datetime($trade['time']);
                if ($trade['direction'] == 's') {
                    $t['sales'][] = ['x'=>$trade['time'], 'y'=>$trade['price']];
                }
                else {
                    $t['purchases'][] = ['x'=>$trade['time'], 'y'=>$trade['price']];
                }
            }
        }

        return $t;
    }

    function decisions($asset_pair) {
        $t['pdecision'] = [];
        $t['sdecision'] = [];

        if (isset($asset_pair['odin']['analyses']['list'])) {
            foreach($this->asset_pair['odin']['analyses']['list'] as $analysis) {
                $analysis['time'] = $this->datetime($analysis['time']);
                if (!empty($analysis['decision'])) {
                    //print_r($analysis['decision']);
                    if ($analysis['decision']['direction'] == 's') {
                        $t['sdecision'][] = ['x'=>$analysis['time'], 'y'=>$analysis['decision']['estimated_price']];
                    }
                    else {
                        $t['pdecision'][] = ['x'=>$analysis['time'], 'y'=>$analysis['decision']['estimated_price']];
                    }
                }
            }
        }

        return $t;
    }

    function analyses($asset_pair) {
        $t = [];

        if (isset($asset_pair['odin']['analyses']['list'])) {
            foreach($this->asset_pair['odin']['analyses']['list'] as $analysis) {
                $analysis['time'] = $this->datetime($analysis['time']);
                if (!empty($analysis)) {
                    //print_r($analysis['decision']);
                    foreach($analysis['calculations'] as $key=>$value) {
                        if (!isset($t[$key])) {
                            $t[$key] = [];
                        }

                        $t[$key][] = ['x'=>$analysis['time'], 'y'=>$value];
                    }
                }
            }
        }

        return $t;
    }

    function actions($asset_pair) {
        $t['paction'] = [];
        $t['saction'] = [];

        if (isset($asset_pair['odin']['actions']['list'])) {
            foreach($this->asset_pair['odin']['actions']['list'] as $action) {
                $action['time'] = $this->datetime($action['time']);
                if (!empty($action)) {
                    //print_r($analysis['decision']);
                    if ($action['direction'] == 's') {
                        $t['saction'][] = ['x'=>$action['time'], 'y'=>$action['price']];
                    }
                    else {
                        $t['paction'][] = ['x'=>$action['time'], 'y'=>$action['price']];
                    }
                }
            }
        }

        return $t;
    }

}
?>