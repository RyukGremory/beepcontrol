"use strict";
// Cicle Chart
Circles.create({
	id:           'task-complete',
	radius:       50,
	value:        80,
	maxValue:     100,
	width:        5,
	text:         function(value){return value + '%';},
	colors:       ['#36a3f7', '#fff'],
	duration:     400,
	wrpClass:     'circles-wrp',
	textClass:    'circles-text',
	styleWrapper: true,
	styleText:    true
})

//Notify
$.notify({
	icon: 'flaticon-alarm-1',
	title: 'Atlantis Lite',
	message: 'Free Bootstrap 4 Admin Dashboard',
},{
	type: 'info',
	placement: {
		from: "bottom",
		align: "right"
	},
	time: 1000,
});

// JQVmap
$('#map-example').vectorMap(
{
	map: 'world_en',
	backgroundColor: 'transparent',
	borderColor: '#fff',
	borderWidth: 2,
	color: '#e4e4e4',
	enableZoom: true,
	hoverColor: '#35cd3a',
	hoverOpacity: null,
	normalizeFunction: 'linear',
	scaleColors: ['#b6d6ff', '#005ace'],
	selectedColor: '#35cd3a',
	selectedRegions: ['ID', 'RU', 'US', 'AU', 'CN', 'BR'],
	showTooltip: true,
	onRegionClick: function(element, code, region)
	{
		return false;
	}
});

//Chart

var myLegendContainer = document.getElementById("myChartLegend");

$("#activeUsersChart").sparkline([112,109,120,107,110,85,87,90,102,109,120,99,110,85,87,94], {
	type: 'bar',
	height: '100',
	barWidth: 9,
	barSpacing: 10,
	barColor: 'rgba(255,255,255,.3)'
});
