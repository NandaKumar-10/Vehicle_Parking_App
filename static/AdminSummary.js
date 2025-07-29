const colorPalette = [
    'rgba(255, 99, 132, 0.7)',
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 159, 64, 0.7)'
];

const backgroundColors = user.map((_, i) => colorPalette[i % colorPalette.length]);

const PriceForAdminCanvas = document.getElementById('PriceAdminSummary')
const OccupiedCanvas = document.getElementById('OccupiedAdminSummary')

const PriceCtx = PriceForAdminCanvas.getContext('2d')
const OccupiedCtx = OccupiedCanvas.getContext('2d')

new Chart(PriceCtx,{
    type: 'pie',
    data: {
        labels: user,
        datasets: [{
            label: 'Total',
            data: price,
            backgroundColor: backgroundColors,
            hoverOffset: 4
        }]
    }
});

new Chart(OccupiedCtx,{
    type: 'bar',
    data:{
        labels: ['No of Spots Occupied','No of Spots not Occupied'],
        datasets: [{
            axis: 'y',
            label: 'Spots',
            data: [Occupied,notOccupied],
            fill: false,
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',

            ],
            borderColor: [
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
    }
});