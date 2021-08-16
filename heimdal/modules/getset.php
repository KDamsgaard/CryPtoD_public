<?php
/*
Project CryPtoD,
Copyright Søren B. Ølholm,
Primary author: Søren B. Ølholm
*/

/* @class GetSet hendles information from browser and server
*
 * Created on 25/06/2009
 * @author Søren Pedersen
 *
 * _GET, _POST, _COOKIE, _SESSION, _SERVER
 * Makes data from _GET, _POST, _COOKIE, _SESSION and Standard value availeble from the header() method
 * Makes data from _SERVER availeble from the server() method
 * Makes all data from any of the above availeble from the getAll() method
 * Input validation of types Integer, Float, String. 
 * Validated types is set with the setStrict() method
 * To fetch validated data use the sheader() method
 */
 class GetSet {
 
 	var $GET;
 	var $POST;
	var $COOKIE;
	var $SESSION;
	var $SERVER;
 	var $STANDARD_VALUE;
	
 	var $BUILD_HEADER;
 	
	/** @fn GetHeader constructor
	*/
 	function GetSet() {
 	
 		
		//Set all data from _GET into constant
		//Set empty array if _GET is NOT set
		if (isset($_GET)) { $this->GET = $_GET; }
		else { $this->GET = array(); }
		
		//Set all data from _POST into constant
		//Set empty array if _POST is NOT set
		if (isset($_POST)) { $this->POST = $_POST; }
		else { $this->POST = array(); }
		
		//Set all data from _COOKIE into constant
		//Set empty array if _COOKIE is NOT set
		if (isset($_COOKIE)) { $this->COOKIE = $_COOKIE; }
		else { $this->COOKIE = array(); }
		
		//Set all data from _SESSION into constant
		//Set empty array if _SESSION is NOT set
		if (isset($_SESSION)) { $this->SESSION = $_SESSION; }
		else { $this->SESSION = array(); }
 		
		//Set all data from _SERVER into constant
		//Set empty array if _SERVER is NOT set
		if (isset($_SERVER)) { $this->SERVER = $_SERVER; }
		else { $this->SERVER = array(); }
		
		$this->STANDARD_VALUE 	= null;
		$this->BUILD_HEADER		= "?";
		
 	}//END function
 	
	//////////////////////////// SETTERS ////////////////////////////
 	
	/** @fn setStandardValue defines a standard value to load if selected field name in "header" or "server" does not exist does not exist
	* @param String $name Name of field in array to store $value
	* @param String $value Value to save in array
	*/
 	public function setStandardValue($name,$value) {
 		$this->STANDARD_VALUE[$name] = $value;
 	}
 	
 	/** Enters a new value into the session array
 	 * 
 	 * @param $name String
 	 * @param $value String
 	 */
 	public function setSession($name,$value) {
 		
 		$_SESSION[$name] = $value;
 		$this->SESSION[$name] = $value;
 		
 	}//END function
 	
 	/** Set/destroy a cookie, if you do not want a time limiter, just set it as null
 	 * 
 	 * @param $name String
 	 * @param $value String
 	 * @param $timer double
 	 */
 	public function setCookie($name,$value,$timer=null) {
 		
 		if ($timer != null) {
 			setcookie($name,$value,time()+$timer);
 		}
 		else {
 			setcookie($name,$value);
 			$this->COOKIE[$name] = $value;
 		}
 		
 	}//END function
 	
	//////////////////////////// PRIVATE GETTERS ////////////////////////////

	/** @fn fetchStandardValue Returns value from selected field if any is found
	* @param String $name Name of field
	* @return String Field value
	*/
 	function fetchStandardValue($name) {
 		$out = "";
 		
 		if (isset($this->STANDARD_VALUE[$name])) { $out = $this->STANDARD_VALUE[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}
 	
	/** @fn fetchGET Fetches any value from $_GET
	* @param String $name Name of field
	* @return String Value of field
	*/
 	private function fetchGET($name) {
 		$out = "";
 		
 		if (isset($this->GET[$name])) { $out = $this->GET[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}//END function
 	
	/** @fn fetchGET Fetches any value from $_GET
	* @param String $name Name of field
	* @return String Value of field
	*/
 	private function fetchPOST($name) {
 		$out = "";
 		
 		if (isset($this->POST[$name])) { $out = $this->POST[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}//END function
 	
	/** @fn fetchGET Fetches any value from $_GET
	* @param String $name Name of field
	* @return String Value of field
	*/
 	private function fetchSessionValue($name) {
 		$out = "";
 		
 		if (isset($this->SESSION[$name])) { $out = $this->SESSION[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}
	
	/** @fn fetchGET Fetches any value from $_GET
	* @param String $name Name of field
	* @return String Value of field
	*/
	private function fetchCookieValue($name) {
 		$out = "";
 		
 		if (isset($this->COOKIE[$name])) { $out = $this->COOKIE[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}
	
	/** @fn fetchGET Fetches any value from $_GET
	* @param String $name Name of field
	* @return String Value of field
	*/
	private function fetchServerValue($name) {
 		$out = "";
 		
 		if (isset($this->SERVER[$name])) { $out = $this->SERVER[$name]; }
 		else { $out = null; }
 		
 		return $out;
 	}

	//////////////////////////// SPECIAL ////////////////////////////
	
	/** @fn makeMD5 Takes a String and returns an md5 hash from it
	*/
	public function makeMD5($string) {
		$out = md5($string);
		
		return $out;
	}//END function
	
	//////////////////////////// HEADER ////////////////////////////
	
	/** @fn header Returns any selected value from _GET and _POST or from standard value if nothing is found
	* @param $name String name of the field to return
	* @return String with selected value
	*/
 	public function header($name) {
 		$out = "";
 		
 		if ($this->fetchPOST($name) != null) { 
 			$out = $this->fetchPOST($name);
 		}
 		elseif ($this->fetchGET($name) != null) {
 			$out = $this->fetchGET($name);
 		}
		elseif ($this->fetchSessionValue($name) != null) {
 			$out = $this->fetchSessionValue($name);
 		}
 		elseif ($this->fetchCookieValue($name) != null) {
 			$out = $this->fetchCookieValue($name);
 		}
 		elseif ($this->fetchStandardValue($name) != null) { 
 			$out = $this->fetchStandardValue($name); 
 		}
 		else {
 			$out = null;
 		}
 		
 		return $out;
 	}//END function
 	
 	/** @fn header Returns an array of values from the provided array of values to fetch
 	 * @param array $array
 	 * @return array
 	 */
 	public function aheader($array) {
 		$out = array();
 		
 		foreach($array as $a) {
 			$out[$a] = $this->header($a);
 		}
 		
 		return $out;
 	}
 	
	/** @fn header Returns any selected value from $_SERVER or from standard value if nothing is found
	* @param $name String name of the field to return
	* @return String with selected value
	*/
 	public function server($name) {
 		$out = "";
 		
 		if ($this->fetchServerValue($name) != null) {
 			$out = $this->fetchServerValue($name);
 		}
 		elseif ($this->fetchStandardValue($name) != null) { 
 			$out = $this->fetchStandardValue($name); 
 		}
 		else {
 			$out = null;
 		}
 		
 		return $out;
 	}//END function
	 	
	/** @fn getAll Returns the entire array of the selected item($_GET,$_POST,$_COOKIE,$_SESSION,$_SERVER or Standard values)
	* @param String $type Witch return type of the above you would like to get
	* @return Array
	*/
	public function getAll($type) {
		$out = "";
		
		switch($type) {
		
			case "get":
				$out = $this->GET;
			break;
			
			case "post":
				$out = $this->POST;
			break;
			
			case "cookie":
				$out = $this->COOKIE;
			break;
			
			case "session":
				$out = $this->SESSION;
			break;
			
			case "server":
				$out = $this->SERVER;
			break;
			
			case "standard":
				$out = $this->STANDARD_VALUE;
			break;
		
			default:
				$out = null;
			break;
		
		}//END switch
		
		return $out;
	}//END function
		
	/** Builds a string ready to be passed to the header
	 *
	 * @param String $name
	 * @param String $value
	 * @param boolean $reset
	 */
	public function buildHeader($name,$value,$reset=false) {
		$out = "";
		$this->BUILD_HEADER .= $name . "=" . $value;
	
		if (!$reset) {
			$this->BUILD_HEADER .= "&";
			$out = $this->BUILD_HEADER;
		}
		else {
			$out = $this->BUILD_HEADER;
			$this->BUILD_HEADER = "?";
		}
	
		return $out;
	}
	//////////////////////////// URL Parser ////////////////////////////

 	/** Parses URL information for correct output
 	 */
  	public function parseURL($url) {
 		$out = "";
 		$parse = "";
 		
 		//Check if string is not empty or contains "http://"
 		if ( ($url != "http://") && ($url != "") ) { $parse = parse_url($url); }
 		
 		if (isset($parse['scheme'])) { $out .= $parse['scheme'] . "://"; }
 		else { $out .= "http://"; }
		
 		if (isset($parse['user']) && (isset($parse['pass']))) { $out .= $parse['user'] . ":" . $parse['pass'] . "@"; }
 		if (isset($parse['host'])) { $out .= $parse['host']; }
 		if (isset($parse['path'])) { $out .= $parse['path']; }
 		if (isset($parse['query'])) { $out .= "?".$parse['query']; }
 		if (isset($parse['fragment'])) { $out .= $parse['fragment']; }
 		
 		return $out;
  	}
 
 } //END class
?>