const UserOccupiedCanvas = document.getElementById('userSummary')
const userctx=UserOccupiedCanvas.getContext('2d')
new Chart(userctx,{
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