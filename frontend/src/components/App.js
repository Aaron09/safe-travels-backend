import React, { Component } from "react";
import CountyInfo from './CountyInfo'

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <CountyInfo id={1} />
        </header>
      </div>
    );
  }
}

export default App;
