
import { Chart as Chartjs, registerables } from "chart.js";
import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Dropdown } from "../dropdown";
import { options, price_filter, dataModel } from "./graph.util";

// const data = {
//     labels: ['10:00AM', '12:00PM', '03:00PM'],
//     datasets: [{
//         label: 'My First Dataset',
//         data: [65, 59, 80],
//         fill: false,
//         borderColor: 'rgb(75, 192, 192)',
//         tension: 0.1
//     }]
// };




Chartjs.register(...registerables);
  
export default ({code, currentFilter, loadingCode, loadError}) => {

    const [data, setData] = useState(dataModel(currentFilter, [], 0));
    const [latestPrice, setLatestPrice] = useState('');

    const msg = code.name || loadError || 'Type something';


    useEffect(() => {
        if (!code.name) {
            setLatestPrice('');
            return;
        }
        const tmp = data;
        const date = new Date();
        const prices = code.prices;
        console.log(prices, code.predicted);
        setData(dataModel(currentFilter, prices, code.predicted))
        setLatestPrice(Number(prices[prices.length - 1]).toFixed(2))
    }, [code.name, code.prices, currentFilter]);
    
    return (
        <div className="h-full w-full flex-1 overflow-x-auto">
        {
            loadingCode
            ?
            <div className="container flex justify-center bg-white mx-auto my-12 p-10 rounded-lg">
                <div className="animate-pulse h-12 w-72 bg-slate-200 rounded-xl"></div>
            </div>
            :
            <>
            <div className="container relative capitalize bg-white mx-auto my-12 p-10 text-gray-500 text-4xl text-center rounded-lg font-light">
                { msg }
                {
                    latestPrice
                    ?
                    <>
                    <span className=" text-3xl"> {latestPrice}</span>
                    <Dropdown />
                    </>
                    :
                    null
                }
            </div>
            {
                code && !loadError
                ?
                <>
                    <div className="container bg-white mx-auto my-12 p-10">
                        <div>
                            <Line data={data} options={options} className="h-full p-10" />
                        </div>
                    </div>
                </>
                :
                null
            }
            </>
        }
        </div>
    );
}