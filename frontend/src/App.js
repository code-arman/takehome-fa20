import React, { Component } from 'react'
import Instructions from './Instructions'
import Restaurant from './Restaurant'
import Counter from './Counter'


class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      restaurants: [
        {id: 1, name: "Golden Harbor", rating: 10},
        {id: 2, name: "Potbelly", rating: 6},
        {id: 3, name: "Noodles and Company", rating: 8},
      ],
      inputValue: ''
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

  }
  

  render() {
    return (
      <div className="App">
        <Counter count={0} />
        <Instructions complete={true}/>
        {this.state.restaurants.map(x => (
          <Restaurant id={x.id} name={x.name} rating={x.rating} />
        ))}
        
        <input value={this.state.inputValue} onChange={ this.handleChange} />  
       <button variant="primary" onClick={this.handleSubmit}>Submit</button>
       
      </div>
    )
  }
handleSubmit(evt) {
    let newRestaurant = {id: this.state.restaurants.length+1, name: this.state.inputValue,rating:0}
    this.setState((prevState) => ({restaurants: [...prevState.restaurants, newRestaurant]}))
  };

  handleChange(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }
}

export default App
