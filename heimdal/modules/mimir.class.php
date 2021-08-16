<?php
class Mimir {
    var $mongo;

    function __construct($mongo) {
        $this->mongo = $mongo;
    }

    function fetch_scores($asset_pair) {
        if (isset($asset_pair['pair_name'])) {
            $db = $this->mongo->db->Mimir;
            $collection = $db->selectCollection($asset_pair['pair_name']);

            $asset_ultimate = $this->mongo->find($collection, ['_id'=>'ultimate'], []);
            if (!empty($asset_ultimate[0])) {
                 $asset_pair['mimir']['scores']['ultimate'] = $asset_ultimate[0]['result'];
            }
            else {
                $asset_pair['mimir']['scores']['ultimate'] = [
                    'scores'=> ['original'=>0, 'degenerated'=>0],
                    'factors'=> [],
                    'analyzer'=>null,
                ];
            }

            return $asset_pair;
        }
        else {
            return null;
        }
    }
}
?>