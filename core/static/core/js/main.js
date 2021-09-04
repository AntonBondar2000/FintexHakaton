var all_collor = []
function getRandomColor() {
    var letters = '0123456789ABCDE'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    if (all_collor.find(el=>el==color) != undefined){
        return getRandomColor()
    }
    all_collor.push(color)
    return color;
}
let keys_branch = Object.keys(branchData)
let values_branch = Object.values(branchData)
let colors_branch = []
for (let i = 0; i<keys_branch.length; i++){
    colors_branch.push(getRandomColor())
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
});
let keys_type = Object.keys(typeData)
let values_type = Object.values(typeData)
let colors_type = []
for (let i = 0; i<keys_type.length; i++){
    colors_type.push(getRandomColor())
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
});

let keys_currency = Object.keys(currencyData)
let values_currency = Object.values(currencyData)
let colors_currency = []
for (let i = 0; i<keys_currency.length; i++){
    colors_currency.push(getRandomColor())
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
});

