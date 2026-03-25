import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


function ProductSearch({ search }) {
  const navigate = useNavigate();
  const [searchData, setSearchData] = useState({
    search: search !== 'none' ? search : '',
  });

  const getSearch = (e) => {
    setSearchData({ ...searchData, [e.target.name]: e.target.value });
  }

  const gameSearch = async (e) => {
    // e.preventDefault();
    navigate('/products/1/none/none/0/4000/' + (searchData.search ? searchData.search : 'none'))
    window.location.reload();
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      gameSearch();
    }
  }

  console.log(searchData)

  return (
    <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
      <div className="input-group">
        <input
          className="form-control"
          name='search'
          type="text"
          placeholder="Search game..."
          aria-label="search input"
          onChange={getSearch}
          onKeyDown={handleKeyDown}
          value={searchData.search}
        />
        <button className="btn btn-outline-dark" onClick={gameSearch}>
          <FontAwesomeIcon icon={["fas", "search"]} />
        </button>
      </div>
    </div>
  );
}

export default ProductSearch;