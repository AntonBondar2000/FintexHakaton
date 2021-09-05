function distinctColors() {
    var r = Math.floor(Math.random()*255);
    var g = Math.floor(Math.random()*255);
    var b = Math.floor(Math.random()*255);
    return "#"+r.toString(16) + g.toString(16) + b.toString(16)
}
let keys_branch = Object.keys(branchData)
let values_branch = Object.values(branchData)
let colors_branch = []
for (let i = 0; i<keys_branch.length; i++){
    colors_branch.push(distinctColors())
}
var ctx = document.getElementById('branch').getContext('2d');
var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: keys_branch,
        datasets: [{
            data: values_branch,
            hoverOffset: 10,
            borderWidth: 0,
            backgroundColor: colors_branch
        }],
    },
    options: {
        title: {
            display: true,
            text: 'Диверсификация по отраслям',
            position: 'bottom',
            fontSize: 16,
            padding: 20
        }
    }
});

let keys_type = Object.keys(typeData)
let values_type = Object.values(typeData)
let colors_type = []
for (let i = 0; i<keys_type.length; i++){
    colors_type.push(distinctColors())
}
var ctx = document.getElementById('type').getContext('2d');
var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: keys_type,
        datasets: [{
            data: values_type,
            hoverOffset: 10,
            borderWidth: 0,
            backgroundColor: colors_type
        }],
    },
    options: {
        title: {
            display: true,
            text: 'Диверсификация по типу актива',
            position: 'bottom',
            fontSize: 16,
            fontColor: '#000',
            padding: 20
        }
    }
});

let keys_currency = Object.keys(currencyData)
let values_currency = Object.values(currencyData)
let colors_currency = []
for (let i = 0; i<keys_currency.length; i++){
    colors_currency.push(distinctColors())
}
var ctx = document.getElementById('currency').getContext('2d');
var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: keys_currency,
        datasets: [{
            data: values_currency,
            hoverOffset: 10,
            borderWidth: 0,
            backgroundColor: colors_currency
        }],
    },
    options: {
        title: {
            display: true,
            text: 'Диверсификация по валюте',
            position: 'bottom',
            fontSize: 16,
            fontColor: '#000',
            padding: 20
        }
    }
});

