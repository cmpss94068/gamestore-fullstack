/* eslint-disable array-callback-return */
import { Link, useParams } from "react-router-dom";
import Product from "./Product";
import Pagination from "./Pagination";
import ProductFilter from "./ProductFilter";
import { useState, useEffect } from "react";
import ScrollToTopOnMount from "../template/ScrollToTopOnMount";
import axios from 'axios';
import ProductSearch from "./ProductSearch";

function ProductList() {
  const [viewType] = useState({ grid: true });
  const [gameData, setGameData] = useState(null);
  const [gameCategory, setGameCategory] = useState(null);
  const [gamePlatform, setGamePlatform] = useState(null);
  const { page, category = '', platform = '', minPrice = 0, maxPrice = 4000, search = '' } = useParams();

  useEffect(() => {
    let gameUrl = 'http://127.0.0.1:8000/api/gameprofile/profilePost/?page=' + page + "&category_name=" + (category === 'none' ? '' : category) + "&platform_name=" + (platform === 'none' ? '' : platform) + "&min_price=" + minPrice + "&max_price=" + maxPrice + "&search=" + (search === 'none' ? '' : search);
    let categoryUrl = 'http://127.0.0.1:8000/api/gameprofile/category/';
    let platformUrl = 'http://127.0.0.1:8000/api/gameprofile/platform/';

    console.log(gameUrl)

    Promise.all([
      axios.get(gameUrl),
      axios.get(categoryUrl),
      axios.get(platformUrl)
    ]).then((responses) => {
      // 解析請求的數據
      const [response1, response2, response3] = responses;
      setGameData(response1.data);
      setGameCategory(response2.data);
      setGamePlatform(response3.data);
    })
  }, [category, maxPrice, minPrice, page, platform, search]);

  if (!gameData || !gamePlatform || !gameCategory) {
    return <div>Loading...</div>;
  }
  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded">
        <ol className="breadcrumb p-3 mb-0">
          <li className="breadcrumb-item">
            <Link
              className="text-decoration-none link-secondary"
              to="/products"
              replace
            >
              All Prodcuts
            </Link>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            Cases &amp; Covers
          </li>
        </ol>
      </nav>

      <div className="h-scroller d-block d-lg-none">
        <nav className="nav h-underline">
          {gameCategory.map((item, index) => {
            return (
              <div key={index} className="h-link me-2">
                <Link
                  // to="/products"
                  className="btn btn-sm btn-outline-dark rounded-pill"
                  replace
                >
                  {item.name}
                </Link>
              </div>
            );
          })}
        </nav>
      </div>

      <div className="row mb-3 d-block d-lg-none">
        <div className="col-12">
          <div id="accordionFilter" className="accordion shadow-sm">
            <div className="accordion-item">
              <h2 className="accordion-header" id="headingOne">
                <button
                  className="accordion-button fw-bold collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapseFilter"
                  aria-expanded="false"
                  aria-controls="collapseFilter"
                >
                  Filter Products
                </button>
              </h2>
            </div>
            <div
              id="collapseFilter"
              className="accordion-collapse collapse"
              data-bs-parent="#accordionFilter"
            >
              <div className="accordion-body p-0">
                <ProductFilter
                  gameCategory={gameCategory}
                  gamePlatform={gamePlatform}
                  categoryUrl={category}
                  platformUrl={platform}
                  minPrice={minPrice}
                  maxPrice={maxPrice}
                  search={search}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row mb-4 mt-lg-3">
        <div className="d-none d-lg-block col-lg-3">
          <div className="border rounded shadow-sm">
            <ProductFilter
              gameCategory={gameCategory}
              gamePlatform={gamePlatform}
              categoryUrl={category}
              platformUrl={platform}
              minPrice={minPrice}
              maxPrice={maxPrice}
              search={search}
            />
          </div>
        </div>
        <div className="col-lg-9">
          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-3 d-none d-lg-block">
                {/* <select
                  className="form-select"
                  aria-label="Default select example"
                  defaultValue=""
                >
                  <option value="">All Models</option>
                  <option value="1">iPhone X</option>
                  <option value="2">iPhone Xs</option>
                  <option value="3">iPhone 11</option>
                </select> */}
              </div>
              <ProductSearch search={search} />
            </div>
            <div
              className={
                "row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 " +
                (viewType.grid ? "row-cols-xl-3" : "row-cols-xl-2")
              }
            >
              {/* {gameData.results.map((game, index) => (
                <div key={index}>
                  <h2>{game.name}</h2>
                </div>
              ))} */}
              {Array.from({ length: 12 }, (_, i) => {
                if (viewType.grid) {
                  if (gameData.results[i] != null) {
                    return (
                      <Product
                        key={i}
                        name={gameData.results[i].game_name}
                        price={gameData.results[i].game_price}
                        img={gameData.results[i].game_img}
                      />);
                  }
                }
              })}
            </div>
            <Pagination
              currentPage={page}
              totalCount={gameData.count}
              totalPages={Math.ceil(gameData.count / 12)}
              category={category}
              platform={platform}
              minPrice={minPrice}
              maxPrice={maxPrice}
              search={search}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductList;
