import React, { Component } from "react"
import axios from 'axios'

const backend_url = "http://127.0.0.1:8000/"

class CreateReview extends Component {
  constructor(props) {
    super(props)
  }

  onPost = (description, rating) => {
    axios.post(backend_url + "review/create/" + this.props.id + '/', {
      description,
      rating
    })
  }

  render() {
    return (
      <div className="App">
        {this.state.data.map((description, rating, timestamp) => (
          <div>
            <div>Name: {description}</div>
            <div>State: {rating}</div>
            <div>Population: {timestamp}</div>
            <br/>
          </div>
        ))}
      </div>
    );
  }
}

export default CreateReview
