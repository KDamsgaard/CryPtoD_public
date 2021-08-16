class CryPtoD_Chart {
    constructor(chart_canvas, chart_colors, update_interval) {
        //this.chart_colors = chart_colors;
        this.chart = this.init_chart(chart_canvas);
        this.update_interval = update_interval;
        this.interval = null;

        this.datasets_infomation = {'labels':[], 'active':{}};

        this.chart_colors = {
            "trades_purchases": "rgb(0, 255, 0, 0.2)",
            "trades_sales": "rgb(255, 0, 0, 0.2)",
            "decisions_purchases": "rgb(100, 255, 0, 0.3)",
            "decisions_sales": "rgb(255, 100, 0, 0.3)",
            "actions_purchases": "rgb(100, 255, 0)",
            "actions_sales": "rgb(255, 100, 0)",
            "short_sma": "rgb(0, 255, 0, 0.6)",
            "short": "rgb(0, 255, 0, 0.6)",
            "long_sma": "rgb(20, 140, 20, 0.7)",
            "long": "rgb(20, 140, 20, 0.7)",
            "tension_sma": "rgb(50, 90, 50)",
            "tension": "rgb(50, 90, 50)",
            "super_short_sma": "rgb(255, 0, 0, 0.3)",
        };
    }

    datasets_labels() { return this.datasets_infomation.labels; }

    datasets_active() { return this.datasets_infomation.active; }

    update() {
        this.chart.update();
    }

    start() {
        this.update();
        this.interval = setInterval(() => this.update(), this.update_interval);
    }

    stop() {
        clearInterval(this.interval);
    }

    // Initialize a new empty chart object
    init_chart(chart_canvas) {
        var ctx = document.getElementById(chart_canvas);
        var cryptod_chart = new Chart(ctx, {
            type: 'line',
            responsive:true,
            maintainAspectRatio: false,
            data: {
                labels: [],
                datasets: []
            },
            options: {
                animation: {
                    duration: 0
                },
                hover: {
                    animationDuration: 0 // duration of animations when hovering an item
                },
                responsiveAnimationDuration: 0, // animation duration after a resize
                scales: {
                    xAxes: [{
                        ticks: {
                            //autoSkip: false,
                            sampleSize: 1,
                            maxRotation: 45,
                            minRotation: 45
                        },
                        type: 'time',
                        time: {
                            tooltipFormat: 'YYYY-MM-DD HH:mm',
                            displayFormats: {
                                millisecond: 'HH:mm:ss.SSS',
                                second: 'HH:mm:ss',
                                minute: 'HH:mm',
                                hour: 'HH'
                            }
                        },
                    }],
                },
                pan: {
                    enabled: true,
                    mode: "xy",
                    speed: 10,
                    threshold: 10
                },
                zoom: {
                    enabled: true,
                    drag: false,
                    mode: "xy",
                    speed: 0.2,
                    sensitivity: 0.5,
                    limits: {
                        max: 10,
                        min: 0.5
                    }
                }
            }
        });

        return cryptod_chart;
    }//END init_chart

    add_dataset(label, color, dataset={}) {
        dataset['type'] = 'scatter';
        dataset['label'] = label;
        dataset['fill'] = false;
        dataset['lineTension'] = 0;
        dataset['data'] = [];
        dataset['hidden'] = false;

        if (this.chart_colors[color] != undefined) {
            dataset['borderColor'] = this.chart_colors[color];
        }
        else {
            var r = Math.random() * (255 - 0) + 0;
            var g = Math.random() * (255 - 0) + 0;
            var b = Math.random() * (255 - 0) + 0;
            dataset['borderColor'] = "rgb("+r+","+g+","+b+")";
        }


        console.log(this.chart_colors[color]);
        //console.log(this.chart_colors);
        this.chart.data.datasets.push(dataset);

        this.datasets_infomation['labels'].push(label);
        this.datasets_infomation['active'][label] = true;
    }//END add_dataset

    dataset_information() { return this.datasets_infomation; }

    enable_dataset(label) {
        if (label in this.datasets_infomation['active']) {
            var index = this.find_dataset_index(label);
            this.datasets_infomation['active'][label] = true;
            this.chart.data.datasets[index].hidden = false;
        }
    }

    disable_dataset(label) {
        if (label in this.datasets_infomation['active']) {
            var index = this.find_dataset_index(label);
            this.datasets_infomation['active'][label] = false;
            this.chart.data.datasets[index].hidden = true;
        }
    }

    update_labels(labels=[]) {
        if (labels.length == 0) { console.log("Warning[update_labels]> labels are empty"); }
        else { this.chart.data.labels = labels; }
    }//END update_labels

    // Locates the dataset index of a label
    find_dataset_index(dataset_label='') {
        var index = null;
        if (dataset_label == '') { console.log("Warning[find_dataset_index]> dataset_label is empty"); }
        else {
            for (var i=0; i<this.chart.data.datasets.length; i++) {
                if (this.chart.data.datasets[i].label == dataset_label) { index = i; }
            }
            if (index == null) { console.log("Warning[find_dataset_index]> dataset label: "+dataset_label+" not found"); }
        }
        return index;
    }//END find_dataset_index

    fill_dataset(dataset_label, plot_key, data) {
        var ds_index = this.find_dataset_index(dataset_label);
        if (ds_index != null) {

            if (data != undefined) {
                if (data.length > 0) {
                    this.chart.data.datasets[ds_index].data = [];

                    if (this.datasets_infomation['active'][dataset_label] == true) {
                        for (var i=0; i<data.length; i++) {
                            var item = data[i];
                            var plot_value = null;
                            var pkey = null;

                            for(var plot_i=0; plot_i<plot_key.length; plot_i++) {
                                pkey = plot_key[plot_i];
                                if (plot_value == null) {
                                    plot_value = item[plot_key[plot_i]];
                                }
                                else {
                                    plot_value = plot_value[plot_key[plot_i]];
                                }
                            }
                            if (plot_value != undefined) {
                                this.chart.data.datasets[ds_index].data.push({x: item.datetime, y: plot_value});
                            }
                        }
                    }
                }
            }
            else {
                console.log("no data to display");
            }

        }
    }//END fill_dataset

    fill_dataset_simplified(dataset_label, data) {
        var ds_index = this.find_dataset_index(dataset_label);
        if (ds_index != null) {

            if (data != undefined) {
                if (data.length > 0) {
                    this.chart.data.datasets[ds_index].data = [];

                    if (this.datasets_infomation['active'][dataset_label] == true) {
                        this.chart.data.datasets[ds_index].data = data;
                    }
                }
            }
            else {
                console.log("no data to display");
            }

        }
    }//END fill_dataset

}//END class

class DynamicChartData {
    constructor(cryptod_chart, asset_pair, update_interval) {
        this.chart = cryptod_chart;
        this.asset_pair = asset_pair;
        this.update_interval = update_interval;
        this.interval = null;
        this.data = null;
    }

    init_chart_datasets() {
        if (this.chart.datasets_labels().length == 0) {
            console.log("Init chart datasets..")
            var main_keys = Object.keys(this.data);
            //var calculations = this.data.analyses.calculations;

            // Add all
            for(var i=0; i<main_keys.length; i++) {
                if (main_keys[i] != 'calculations' && main_keys[i] != 'labels') {
                    var sub_keys = Object.keys(this.data[main_keys[i]]);

                    for(var j=0; j<sub_keys.length; j++) {
                        var r = 0;
                        var g = 0;
                        var b = 0;
                        var color = "";
                        console.log('KEY-->' + main_keys[i] +'/'+sub_keys[j]);
                        if (sub_keys[j].includes('purchase') > 0) {
                            g = Math.random() * (255 - 100) + 100;
                            r = Math.random() * (50 - 0) + 0;
                        }
                        else if (sub_keys[j].includes('sales') > 0) {
                            r = Math.random() * (255 - 150) + 150;
                            g = Math.random() * (50 - 0) + 0;
                        }
                        else {
                        console.log("random color");
                            r = Math.random() * (255 - 0) + 0;
                            g = Math.random() * (255 - 0) + 0;
                            b = Math.random() * (255 - 0) + 0;
                        }
                        color = "rgb("+r+","+g+","+b+")";
                        console.log("color: " + color);
                        var dataset_name = main_keys[i]+'_'+sub_keys[j];
                        var color = this.data[main_keys[i]][sub_keys[j]]['color'];
                        var style = this.data[main_keys[i]][sub_keys[j]]['style'];
                        console.log("color "+color+" style " + style);
                        this.chart.add_dataset(dataset_name, color,style);
                    }
                }
            }

            if (this.data.calculations != undefined) {
                var calculations = this.data.calculations;
                var calc_keys = Object.keys(calculations);
                for (var i=0; i<calc_keys.length; i++) {
                    var r = Math.random() * (255 - 0) + 0;
                    var g = Math.random() * (255 - 0) + 0;
                    var b = 255;
                    var color = "rgb("+r+","+g+","+b+")";
                    var dataset_name = calc_keys[i];
                    this.chart.add_dataset(dataset_name, color,{pointRadius: 0, borderWidth: 1,showLine: true});
                }
            }

        }

    }


    start() {
        //this.fetch_data();
        //this.interval = setInterval(() => this.update(), this.update_interval);
        this.update();
    }

    stop() {
        clearInterval(this.interval);
    }

    update() {
        this.fetch_data();
    }

    fill_labels() {
        if (this.data.labels.length > 0) {
            console.log("Filling labels");
            this.chart.update_labels(this.data.labels);
        }
    }

    fill_datasets2() {
        this.init_chart_datasets();
        var main_keys = Object.keys(this.data);

        for(var i=0; i<main_keys.length; i++) {
            if (main_keys[i] != 'calculations' && main_keys[i] != 'labels') {
                var sub_keys = Object.keys(this.data[main_keys[i]]);
                for(var j=0; j<sub_keys.length; j++) {
                    console.log('KEY-->' + main_keys[i] +'/'+sub_keys[j]);
                    var dataset_name = main_keys[i]+'_'+sub_keys[j];
                    //this.chart.add_dataset(dataset_name, 'color_purchases',{pointStyle: 'rect',radius: 2,showLine: false});
                    this.chart.fill_dataset_simplified(dataset_name, this.data[main_keys[i]][sub_keys[j]]['data']);
                }
            }
        }

        if (this.data.calculations != undefined) {
            var calculations = this.data.calculations;
            var calc_keys = Object.keys(calculations);
            for (var i=0; i<calc_keys.length; i++) {
                var dataset_name = calc_keys[i];
                //this.chart.add_dataset(dataset_name, 'color_purchases',{pointStyle: 'rect',radius: 2,showLine: false});
                this.chart.fill_dataset_simplified(dataset_name, calculations[calc_keys[i]]);
            }
        }

    }

    fill_datasets() {
        console.log("Filling datasets");
        /*
        this.chart.fill_dataset('Purchases',['price'], this.data.trades.purchases);
        this.chart.fill_dataset('Sales',['price'], this.data.trades.sales);
        this.chart.fill_dataset('PShort',['smas','short'], this.data.analyses.purchases);
        this.chart.fill_dataset('PLong',['smas','long'], this.data.analyses.purchases);
        this.chart.fill_dataset('PTension',['smas','tension'], this.data.analyses.purchases);
        //this.chart.fill_dataset('SShort',['smas','short'], this.data.analyses.sales);
        //this.chart.fill_dataset('SLong',['smas','long'], this.data.analyses.sales);
        //this.chart.fill_dataset('STension',['smas','tension'], this.data.analyses.sales);
        this.chart.fill_dataset('PDecisions',['estimated_price'], this.data.decisions.purchases);
        this.chart.fill_dataset('SDecisions',['estimated_price'], this.data.decisions.sales);
        this.chart.fill_dataset('PActions',['price'], this.data.actions.purchases);
        this.chart.fill_dataset('SActions',['price'], this.data.actions.sales);
        */


//        this.chart.fill_dataset_simplified('Purchases', this.data.trades.purchases);
//        this.chart.fill_dataset_simplified('Sales', this.data.trades.sales);
//        this.chart.fill_dataset_simplified('PShort', this.data.analyses.purchases.short);
//        this.chart.fill_dataset_simplified('PLong', this.data.analyses.purchases.long);
//        this.chart.fill_dataset_simplified('PTension', this.data.analyses.purchases.tension);
//        this.chart.fill_dataset_simplified('SShort', this.data.analyses.sales.short);
//        this.chart.fill_dataset_simplified('SLong', this.data.analyses.sales.long);
//        this.chart.fill_dataset_simplified('STension', this.data.analyses.sales.tension);
//        this.chart.fill_dataset_simplified('PDecisions', this.data.decisions.purchases);
//        this.chart.fill_dataset_simplified('SDecisions', this.data.decisions.sales);
//        this.chart.fill_dataset_simplified('PActions', this.data.actions.purchases);
//        this.chart.fill_dataset_simplified('SActions', this.data.actions.sales);



        console.log("Filling data done");
    }

    ensure_done(data) {
		return data;
	}

    fetch_data() {
        jQuery.getJSON('endpoint.php?page=graphdata3&asset_pair='+this.asset_pair, function(data) {
			this.data = this.ensure_done(data);
			console.log(this.data);

			if (this.data != null) {
                this.fill_datasets2();
                this.fill_labels();
                //this.fill_datasets();
                //this.chart.update();
            }

            setTimeout(() => this.update(), this.update_interval);
		}.bind(this));
    }

}
