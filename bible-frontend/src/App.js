import React, {useState, useEffect} from 'react'

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

function App() {
    return (
        <div className="App">

            <h1 className="text-success">  SIC'EM NLP</h1>
            <div class="container">
                <div className="row">
                    <div className="col s12 m6">
                        <div className="dropdown">
                            <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Language
                            </button>
                            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <a className="dropdown-item" href="#">English</a>
                                <a className="dropdown-item" href="#">Chinese</a>
                                <a className="dropdown-item" href="#">Hebrew</a>
                            </div>
                        </div>
                        <div className="form-group">
                            <textarea className="form-control" id="exampleFormControlTextarea1" rows="5"></textarea>
                        </div>
                        <a
                            className="btn btn-primary"
                            data-bs-toggle="collapse"
                            href="#collapseExample"
                            role="button"
                            aria-expanded="false"
                            aria-controls="collapseExample"
                        >
                            Translate
                        </a>
                    </div>
                    <div className="col s12 m6">
                       <div className="dropdown">
                            <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Language
                            </button>
                            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <a className="dropdown-item" href="#">English</a>
                                <a className="dropdown-item" href="#">Chinese</a>
                                <a className="dropdown-item" href="#">Hebrew</a>
                            </div>
                        </div>
                        <div className="form-group">
                            <textarea className="form-control" id="exampleFormControlTextarea1" rows="5"></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;



