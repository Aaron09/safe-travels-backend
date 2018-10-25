import React, { Component } from "react"
import axios from 'axios'

const backend_url = "http://127.0.0.1:8000/"

class ReviewInfo extends Component {
  constructor(props) {
    super(props)
    this.state = { data: [] }
  }

  componentDidMount() {
    axios.get(backend_url + "review/all/" + this.props.id).then(response => {
      this.setState({
        data: response.data.reviews
      })
    }).catch(e => {
      console.log(e)
    })
  }

  render() {
    return (
      <div className="App">
        {this.state.data.map((description, rating, timestamp) => (
          <div>
            <div>Description: {description}</div>
            <div>Rating: {rating}</div>
            <div>Timestamp: {timestamp}</div>
            <br/>
          </div>
        ))}
      </div>
    );
  }
}

export default ReviewInfo
