import React, { Component } from 'react';
import { render } from 'react-dom';
import Plot from 'react-plotly.js'
import openSocket from 'socket.io-client';
const socket = openSocket('http://testpi.local:8888');

socket.on('connect', e => console.log(e));
socket.on('sensor_data', e => console.log(e.unit, e.value));

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      data: []
    }
  }

  componentDidMount() {
    socket.on('sensor_data', e => {
      this.setState((prevState) => {
        const data = prevState.data
        data.push(e)
        return { data };
      })
    })
  }

  start = () => {
    socket.emit('sensor_start');
  }

  stop = () => {
    socket.emit('sensor_stop');
    this.setState({ data: [] })
  }

  plotData = () => {
    const { data } = this.state
    console.log(data)
    var dataWindow = data.slice(Math.max(data.length - 100, 1));
    return (
      <Plot
        data={[
          {
            type: 'scatter',
            x: dataWindow.map(d => d.unit),
            y: dataWindow.map(d => d.value)
          }
        ]}

        layout={{
          width: 800,
          height: 600,
          title: 'Photoresistor data'
        }}
      />
    )
  }

  render() {
    const { data } = this.state
    return (
      <div>
        hello
        <button onClick={this.start}>Start</button>
        <button onClick={this.stop}>Stop</button>
        {this.plotData()}
      </div>
    );
  }
}

const root = document.getElementById('root')
render(<App />, root);
