<?php
class Odin {
    var $mongo;
    var $watched;

    function __construct($mongo) {
        $this->mongo = $mongo;
        $this->watched = $this->fetch_watched();
    }

    private function fetch_watched() {
        $collection = $this->mongo->db->Odin;

        $project = array('projection'=>['_id'=>false, 'watched_pairs'=>true]);

        $out = $this->mongo->find($collection->settings, ['_id'=>'system_settings'], $project);
        if (!empty($out)) {
            return $out[0]['watched_pairs'];
        }
        else {
            return null;
        }
    }

    function fetch_trades($asset_pair) {
        if (isset($asset_pair['pair_name'])) {
            $collection = $this->mongo->db->Odin->selectCollection($asset_pair['pair_name']);
            $trades = $this->mongo->find($collection, ['_id'=>'trades'], ['projection'=>['_id'=>0]]);
            if (!empty($trades)) { $trades = $trades[0]['list']; }
            else { return null; }

            return $trades;
        }
        else {
            return null;
        }
    }

    function fetch_analyses($asset_pair) {
        $collection = $this->mongo->db->Odin->selectCollection($asset_pair['pair_name']);
        $analyses = $this->mongo->find($collection, ['_id'=>'analyses'], ['projection'=>['_id'=>0]]);
        //print('fetch_analyses');
        //print_r($analyses);
        if (!empty($analyses)) { $analyses = $analyses[0]['list']; }
        else { return null; }

        return $analyses;
    }

    function fetch_actions($asset_pair) {
        $collection = $this->mongo->db->Odin->selectCollection($asset_pair['pair_name']);
        $analyses = $this->mongo->find($collection, ['_id'=>'actions'], ['projection'=>['_id'=>0]]);
        if (!empty($analyses)) { $analyses = $analyses[0]['list']; }
        else { return null; }

        return $analyses;
    }

    function is_watched($asset_pair, $add=false) {
        if (!$add) { return in_array($asset_pair['pair_name'], $this->watched); }
        else {
            if (is_array($this->watched)) {
                $asset_pair['odin']['watched'] = in_array($asset_pair['pair_name'], $this->watched);
                return $asset_pair;
            }
            else {
                return null;
            }
        }
    }

    function wallet($asset_pair) {
        if (isset($asset_pair['pair_name'])) {
            $collection = $this->mongo->db->Odin->selectCollection($asset_pair['pair_name']);
            $wallet = $this->mongo->find($collection, ['_id'=>'wallet'], ['projection'=>['_id'=>0]]);
            if ($wallet != null) {
                $asset_pair['odin']['wallet'] = $wallet[0];
            }
            else {
                $asset_pair['odin']['wallet'] = ['purse'=>0, 'coins'=>0, 'profit'=>0];
            }
            return $asset_pair;
        }
        else {
            return null;
        }
    }

    function trades_info($asset_pair) {
        $trades = $this->fetch_trades($asset_pair);
        $_trades = [];
        if ($trades != null) {
            $hour_span = ($trades[count($trades)-1]['time'] - $trades[0]['time']) / 60 / 60;
            $_trades['trades_hour_span'] = round($hour_span);
            $_trades['trades'] = count($trades);
            if ($hour_span >= 1) { $_trades['trades_hour'] = round(count($trades) / $hour_span); }
            else { $_trades['trades_hour'] = 0; }
        }
        else {
            $_trades['trades'] = 0;
            $_trades['trades_hour_span'] = 0;
            $_trades['trades_hour'] = 0;
        }

        if (!empty($_trades)) {
            $asset_pair['odin']['trades']['info'] = $_trades;
        }
        else {
            $asset_pair['odin']['trades']['info'] = ['trades'=>0, 'trades_hour_span'=>0, 'trades_hour'=>0];
        }

        return $asset_pair;
    }

    function analyses_info($asset_pair) {
        $analyses = $this->fetch_trades($asset_pair);
        $_trades = [];
        if ($analyses != null) {
            $hour_span = ($analyses[count($analyses)-1]['time'] - $analyses[0]['time']) / 60 / 60;
            $_trades['analyses_hour_span'] = round($hour_span);
            $_trades['analyses'] = count($analyses);
            if ($hour_span) { $_trades['analyses_hour'] = round(count($analyses) / $hour_span); }
        }
        else {
            $_trades['analyses'] = 0;
            $_trades['analyses_hour_span'] = 0;
            $_trades['analyses_hour'] = 0;
        }

        if (!empty($_trades)) {
            $asset_pair['odin']['analyses']['info'] = $_trades;
        }
        else {
            $asset_pair['odin']['analyses']['info'] = ['analyses'=>0, 'analyses_hour_span'=>0, 'analyses_hour'=>0];
        }

        return $asset_pair;
    }

}
?>