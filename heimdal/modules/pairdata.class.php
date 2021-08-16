<?php
require 'modules/chartdata.class.php';

function cmp($a, $b) {
       if ($b['mimir']['scores']['ultimate']['scores']['original'] > 0 && $a['mimir']['scores']['ultimate']['scores']['original'] > 0) {
           return ($b['mimir']['scores']['ultimate']['scores']['original']
                    <=>
                    $a['mimir']['scores']['ultimate']['scores']['original']
                    ||
                    $b['saerimner']['trades']['info']['trades']
                    <=>
                    $a['saerimner']['trades']['info']['trades']
                    );
       }
       else {
            return ($b['saerimner']['trades']['info']['trades']
                    <=>
                    $a['saerimner']['trades']['info']['trades']
                    );
       }
}

class PairData {
    var $mongo;

    var $saerimner;
    var $mimir;
    var $odin;

    var $pairdata;

    function __construct($_mongo) {
        $this->mongo = $_mongo;
        $this->saerimner = new Saerimner($_mongo);
        $this->mimir = new Mimir($_mongo);
        $this->odin = new Odin($_mongo);

        $this->pairdata = ['watched'=>[], 'available'=>[]];
    }

    function sort_scores($list) {
        usort($list, 'cmp');

        return $list;
    }

    function pair_info($pair_name) {
        $asset_pair = null;
        foreach($this->saerimner->available as $_asset_pair) {
            if ($_asset_pair['pair_name'] == $pair_name) {
                $asset_pair = $_asset_pair;
                break;
            }
        }

        $asset_pair = $this->odin->is_watched($asset_pair, true);
        $asset_pair = $this->odin->trades_info($asset_pair);
        $asset_pair = $this->odin->analyses_info($asset_pair);
        $asset_pair = $this->odin->wallet($asset_pair);
        $asset_pair = $this->mimir->fetch_scores($asset_pair);

        $asset_pair['odin']['trades']['list'] = $this->odin->fetch_trades($asset_pair);
        $asset_pair['odin']['actions']['list'] = $this->odin->fetch_actions($asset_pair);
        $asset_pair['odin']['analyses']['list'] = $this->odin->fetch_analyses($asset_pair);
        $asset_pair = (new ChartData($asset_pair))->asset_pair;

        return $asset_pair;
    }

    function build_info_list() {
        foreach($this->saerimner->available as $asset_pair) {
            $asset_pair = $this->odin->is_watched($asset_pair, true);
            $asset_pair = $this->odin->trades_info($asset_pair);
            $asset_pair = $this->odin->analyses_info($asset_pair);
            $asset_pair = $this->odin->wallet($asset_pair);
            $asset_pair = $this->mimir->fetch_scores($asset_pair);

            if (isset($asset_pair['odin'])) {
                // Add the asset_pair to either watched or available lists
                if ($asset_pair['odin']['watched']) { $this->pairdata['watched'][] = $asset_pair; }
                else { $this->pairdata['available'][] = $asset_pair; }
            }
        }

        //$_w_scores = array_column($this->pairdata['watched'], 'ultimate_score');
        //array_multisort($_scores, SORT_DESC, $pair_data);

        $this->pairdata['watched'] = $this->sort_scores($this->pairdata['watched']);
        $this->pairdata['available'] = $this->sort_scores($this->pairdata['available']);
    }

    function build_chart_object($pair_name) {
        $asset_pair = null;
        foreach($this->saerimner->available as $_asset_pair) {
            if ($pair_name == $_asset_pair['pair_name']) {
                $asset_pair = $_asset_pair;
                break;
            }
        }

        if ($asset_pair != null) {
            //TODO add data
            $asset_pair = $this->odin->is_watched($asset_pair, true);
            $asset_pair = $this->odin->trades_info($asset_pair);
            $asset_pair = $this->odin->analyses_info($asset_pair);
            $asset_pair['odin']['trades']['list'] = $this->odin->fetch_trades($asset_pair);
            $asset_pair['odin']['actions']['list'] = $this->odin->fetch_actions($asset_pair);
            //print("'actions'");
            //print_r($asset_pair['odin']['actions']['list']);
            $asset_pair['odin']['analyses']['list'] = $this->odin->fetch_analyses($asset_pair);
            //print_r($asset_pair);

            //$asset_pair = $this->odin->trades_info($asset_pair);
            $asset_pair = $this->odin->wallet($asset_pair);
            $asset_pair = $this->mimir->fetch_scores($asset_pair);

            $asset_pair = (new ChartData($asset_pair))->asset_pair;
        }
        return $asset_pair;
    }

    function get_pair_data($pair_name) {
        $asset_pair = null;
        foreach($this->pairdata['watched'] as $pair) {
            if ($pair['pair_name'] == $pair_name) { $asset_pair = $pair; }
        }

        if ($asset_pair == null) {
            foreach($this->pairdata['available'] as $pair) {
                if ($pair['pair_name'] == $pair_name) { $asset_pair = $pair; }
            }
        }

        return $asset_pair;
    }


}
?>