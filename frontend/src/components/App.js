import React, { Component } from "react";
import CountyInfo from './CountyInfo'
import CreateReview from './CreateReview'
import ReviewInfo from './ReviewInfo'

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <CreateReview id={1} />
          <ReviewInfo id={1} />
        </header>
      </div>
    );
  }
}

export default App;
