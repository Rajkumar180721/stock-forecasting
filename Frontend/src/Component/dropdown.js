


export function Dropdown() {

    const download = (from, to) => {
        window.open(`http://127.0.0.1:5000/getMonthlyReport?from=${from}&to=${to}`, "_self");
    }
    
    return (
        <span className="group absolute right-10 top-0 bottom-0 h-max text-2xl text-white font-normal p-5 mx-5 my-auto cursor-pointer bg-blue-500 rounded-lg after:content-['˅'] after:ml-2">
            Report
            <div className="hidden group-hover:block absolute w-auto min-w-max top-full right-0 text-black bg-gray-50 overflow-hidden rounded-lg shadow-xl">
                <div onClick={() => download('2022-09-01', '2022-09-30')} className="w-full py-4 px-8 bg-gray-50 hover:bg-gray-200">September</div>
                <div onClick={() => download('2022-10-01', '2022-10-30')} className="w-full py-4 px-8 bg-gray-50 hover:bg-gray-200">October</div>
                <div onClick={() => download('2022-11-01', '2022-11-30')} className="w-full py-4 px-8 bg-gray-50 hover:bg-gray-200">November</div>
            </div>
        </span>
    );
}