import React from 'react';
import { useNavigate } from 'react-router-dom';

function Pagination(props) {
    const navigate = useNavigate();

    function changePage(value) {
        navigate('/products/' + value + '/' + props.category + '/' + props.platform + '/' + props.minPrice + '/' + props.maxPrice + '/' + props.search);
        window.location.reload();
    }

    return (
        <div className="d-flex align-items-center mt-auto">
            <nav aria-label="Page navigation example" className="ms-auto">
                <ul className="pagination my-0">
                    {Array.from({ length: props.totalPages }, (_, i) => {
                        if (
                            i + 1 === props.currentPage ||
                            i + 1 === 1 ||
                            i + 1 === props.totalPages ||
                            Math.abs(i + 1 - props.currentPage) <= 2
                        ) {
                            return (
                                <li key={i} className="page-item">
                                    <button className="page-link" onClick={() => changePage(i + 1)}>
                                        {i + 1}
                                    </button>
                                </li>
                            );
                        } else if (i === 1 || i === props.totalPages - 2) {
                            return (
                                <li key={i} className="page-item">
                                    <button className="page-link">
                                        ...
                                    </button>
                                </li>
                            );
                        }
                        return null;
                    })}
                </ul>
            </nav>
        </div >
    );
}

export default Pagination;