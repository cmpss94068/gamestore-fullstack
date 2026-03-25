import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ProductFilter({ gameCategory, gamePlatform, categoryUrl, platformUrl, minPrice, maxPrice, search }) {
    const navigate = useNavigate();
    const [filterData, setFilterData] = useState({
        category: categoryUrl && categoryUrl !== 'none' ? categoryUrl.split(',') : [],
        platform: platformUrl && platformUrl !== 'none' ? platformUrl.split(',') : [],
        minPrice: minPrice,
        maxPrice: maxPrice,
        search: search
    });

    const getCategory = (category) => {
        if (filterData.category.includes(category)) {
            setFilterData({ ...filterData, category: filterData.category.filter(item => item !== category) });
        } else {
            setFilterData({ ...filterData, category: [...filterData.category, category] });
        }
    }

    const getPlatform = (platform) => {
        if (filterData.platform.includes(platform)) {
            setFilterData({ ...filterData, platform: filterData.platform.filter(item => item !== platform) });
        } else {
            setFilterData({ ...filterData, platform: [...filterData.platform, platform] });
        }
    }

    const getPriceChange = (e) => {
        setFilterData({ ...filterData, [e.target.name]: e.target.value });
    };

    const gameFilter = async (e) => {
        e.preventDefault();
        navigate('/products/1/' + (filterData.category.join(',') === '' ? 'none' : filterData.category.join(',')) + '/' + (filterData.platform.join(',') === '' ? 'none' : filterData.platform.join(',')) + '/' + filterData.minPrice + '/' + filterData.maxPrice + '/' + (filterData.search === '' ? 'none' : filterData.search));
    }

    return (
        <ul className="list-group list-group-flush rounded">
            <li className="list-group-item d-none d-lg-block">
                <h5 className="mt-1 mb-2">類別</h5>
                <div className="d-flex flex-wrap my-2">
                    {gameCategory
                        .filter(item => item.name && item.name !== "角色扮演遊戲" && item.name !== '模擬遊戲' && item.name !== '腦力訓練' && item.name !== '模擬器')
                        .map((item, index) => {
                            return (
                                <button
                                    key={index}
                                    className={`btn btn-sm rounded-pill me-2 mb-2 ${filterData.category.includes(item.name) ? 'btn-dark' : 'btn-outline-dark'}`}
                                    onClick={() => getCategory(item.name)}
                                >
                                    {item.name}
                                </button>
                            );
                        })}
                </div>
            </li>
            <li className="list-group-item">
                <h5 className="mt-1 mb-1">遊戲平台</h5>
                <div className="d-flex flex-wrap my-2">
                    {gamePlatform.map((item, index) => {
                        return (
                            <button
                                key={index}
                                className={`btn btn-sm rounded-pill me-2 mb-2 ${filterData.platform.includes(item.name) ? 'btn-dark' : 'btn-outline-dark'}`}
                                onClick={() => getPlatform(item.name)}
                            >
                                {item.name}
                            </button>
                        );
                    })}
                </div>
            </li>
            <li className="list-group-item">
                <h5 className="mt-1 mb-2">價格</h5>
                <div className="d-grid d-block mb-3">
                    <div className="form-floating mb-2">
                        <input
                            type="number"
                            className="form-control"
                            name="minPrice"
                            value={filterData.minPrice}
                            onChange={getPriceChange}
                        />
                        <label htmlFor="floatingInput">最小價格</label>
                    </div>
                    <div className="form-floating mb-2">
                        <input
                            type="number"
                            className="form-control"
                            name="maxPrice"
                            value={filterData.maxPrice}
                            onChange={getPriceChange}
                        />
                        <label htmlFor="floatingInput">最大價格</label>
                    </div>
                    <button className="btn btn-dark" onClick={gameFilter}>搜尋</button>
                </div>
            </li>
        </ul>
    );
}

export default ProductFilter;