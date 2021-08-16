<?php
/*
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
*/

/** Reference links:
* Cursor objects to array https://stackoverflow.com/questions/7670036/convert-a-mongocursor-from-find-to-an-array
*
**/

    class MongoDB {
        var $db;
        private $options;

        function __construct($db_host, $db_port) {
            $this->db = new MongoDB\Client("mongodb://".$db_host.":".$db_port."/", [], ["typeMap" => ['root' => 'array', 'document' => 'array']]);
            $this->options = ["typeMap" => ['root' => 'array', 'document' => 'array']];
        }

        function options() { return $this->options; }

        function collection_names($target) {
            $collections = [];
            foreach($target->listCollections() as $collection) {
                $collections[] = $collection['name'];
            }

            return $collections;
        }

        function find($target, $filter, $options, $sort=array()) {
            $cursor = $target->find($filter, $options);
            $out = [];
            foreach($cursor as $i=>$item) { $out[$i] = $item; }
            return $out;
        }

        function findOne($target, $filter, $options) {
            return $target->findOne($filter, $options);
        }

        function aggregate($target, $filter, $project=[]) {
            return $this->toArray($target->aggregate($filter, $project));
        }

        function update($target, $filter, $query) {
            $target->updateMany($filter, $query);
        }

        function toArray($cursor) {
            $out = array();
            foreach($cursor as $item) {
                $out[] = $item;
            }

            return $out;
        }
    }
?>