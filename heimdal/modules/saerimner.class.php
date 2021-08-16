<?php
class Saerimner {
    var $mongo;
    var $available;

    function __construct($mongo) {
        $this->mongo = $mongo;
        $this->available = $this->load_pair_info();
    }

    private function load_pair_info() {
        $pairs = [];
        foreach($this->fetch_available_pairs() as $pair_name) {
            $pair_data = $this->fetch_pair_info($pair_name);
            if ($pair_data != null) {
                $pair_data['saerimner']['trades']['info'] = $this->build_trades_info($pair_name);
                $pairs[] = $pair_data;
            }
        }
        return $pairs;
    }

    private function fetch_available_pairs() {
        $db = $this->mongo->db->Saerimner;
        $cnames = $this->mongo->collection_names($db);

        return $cnames;
    }

    private function fetch_pair_info($pair_name) {
        $collection = $this->mongo->db->Saerimner->selectCollection($pair_name);
        $pair = $this->mongo->find($collection, ['_id'=>'info'], ['projection'=>['_id'=>0]]);
        if (!empty($pair)) { $pair = $pair[0]; }
        else { return null; }

        return $pair;
    }

    private function build_trades_info($pair_name) {
        $trades = $this->fetch_trades($pair_name);
        $_trades = [];
        if ($trades != null) {
            $hour_span = ($trades[count($trades)-1]['time'] - $trades[0]['time']) / 60 / 60;
            $_trades['trades_hour_span'] = round($hour_span);
            $_trades['trades'] = count($trades);
            if ($hour_span >= 1) { $_trades['trades_hour'] = round(count($trades) / $hour_span); }
            else { $_trades['trades_hour'] = $_trades['trades']; }
        }
        else {
            $_trades['trades'] = 0;
            $_trades['trades_hour_span'] = 0;
            $_trades['trades_hour'] = 0;
        }

        return $_trades;
    }

    function fetch_trades($pair_name) {
        $collection = $this->mongo->db->Saerimner->selectCollection($pair_name);
        $trades = $this->mongo->find($collection, ['_id'=>'trades'], ['projection'=>['_id'=>0]]);
        if (!empty($trades)) { $trades = $trades[0]['list']; }
        else { return null; }

        return $trades;
    }
}
?>