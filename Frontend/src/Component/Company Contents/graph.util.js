

export const price_filter = {
    'Today': ['Yesterday', 'Today', 'Tomorrow'],
    'Week': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    'Month': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
};

export const getLabel = (filter) => {
    if (filter === 'Today')
        return price_filter['Today'];
    
    const event = new Date();
    if (filter === 'Week') {
        let start = event.getDay();
        const weeks = [...Array(8).keys()].map(arr => price_filter['Week'][(start + arr) % 7])
        return weeks;
    }
    if (filter === 'Month') 
        return price_filter['Month']
}

export const dataModel = (filter, prices, predicted) => {
    return {
        labels: getLabel(filter),
        datasets: [
          {
            label: 'Actual',
            data: [...prices],
            borderColor: 'rgb(75, 192, 192)',
            // yAxisID: 'y',
          },
          {
            label: 'predicted',
            data: [...prices, predicted],
            borderColor: '#B9BBB6',
            // yAxisID: 'y1',
          }
        ]
      }
}

export const options =  {
    responsive: true,
    interaction: {
    mode: 'index',
    intersect: false,
    },
    stacked: false,
    plugins: {
    title: {
        display: true,
        text: ''
    }
    },
    // scales: {
    // y: {
    //     type: 'linear',
    //     display: true,
    //     position: 'left',
    // },
    // y1: {
    //     type: 'linear',
    //     display: true,
    //     position: 'left',

    //     // grid line settings
    //     grid: {
    //         drawOnChartArea: false,
    //     },
    // },
    // }
};
