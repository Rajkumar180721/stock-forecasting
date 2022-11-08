

export default ({setCode, currentFilter, changeFilter}) => {


    return (
        <div className="flex flex-col justify-center h-auto w-full p-10 bg-blue-500" >
            <div className="text-5xl mb-3 text-white text-center" >
                Forecast
            </div>
            <div className="mx-auto mt-6" >
                <input className="shadow appearance-none border rounded-full py-5 px-12 text-gray-700 leading-tight uppercase focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Search by Stock code" name="stockForecasting-stockID" size={15} onChange={(e) => setCode(e.target.value, currentFilter)} />
            </div>
            <div className="mx-auto mt-6 text-white">
                <div data-selected={currentFilter === 'Today'} className="inline-block mx-4 my-2 font-light cursor-pointer border-b-2 border-transparent data-[selected=true]:border-white data-[selected=true]:font-normal" onClick={() => changeFilter('Today')}>Today</div>
                <div data-selected={currentFilter === 'Week'} className="inline-block mx-4 my-2 font-light cursor-pointer border-b-2 border-transparent data-[selected=true]:border-white data-[selected=true]:font-normal " onClick={() => changeFilter('Week')}>Week</div>
                <div data-selected={currentFilter === 'Month'} className="inline-block mx-4 my-2 font-light cursor-pointer border-b-2 border-transparent data-[selected=true]:border-white data-[selected=true]:font-normal" onClick={() => changeFilter('Month')}>Month</div>
            </div>
        </div>
    );
}