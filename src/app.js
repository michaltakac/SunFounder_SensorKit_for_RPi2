import 'aframe'
import React, { Component } from 'react';
import { render } from 'react-dom';
import { Scene, Entity } from 'aframe-react'
import Plot from 'react-plotly.js'
import openSocket from 'socket.io-client';

import './styles/main.css'

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
          height: 500,
          title: 'Photoresistor data',
          yaxis: {
            title: 'y-axis title',
            range: [0, 250]
          }
        }}
      />
    )
  }

  renderWebVR () {
    const { data } = this.state
    const lightIntensity = data && data[data.length-1] ? Math.abs((data[data.length-1].value / 10) - 10) : 2
    return (
      <Scene embedded fog>
        <a-assets>
          <img id="groundTexture" src="https://cdn.aframe.io/a-painter/images/floor.jpg"/>
          <img id="skyTexture" src="https://cdn.aframe.io/a-painter/images/sky.jpg"/>
        </a-assets>
        <Entity primitive="a-plane" src="#groundTexture" rotation="-90 0 0" height="100" width="100"/>
        <Entity primitive="a-light" type="ambient" color="#445451"/>
        <Entity
          primitive="a-light"
          type="spot"
          intensity={lightIntensity}
          position="3.31 1.17 -1.98"
          rotation="6.47 -89.84 30"
          penumbra="1"
        />
        <Entity
          primitive="a-light"
          type="spot"
          intensity={lightIntensity}
          position="3.31 1.17 -4"
          rotation="6.47 -89.84 30"
          penumbra="1"
        />
        <Entity primitive="a-sky" height="2048" radius="30" src="#skyTexture" theta-length="90" width="2048"/>
        <Entity particle-system={{preset: 'snow', particleCount: 2000}}/>
        <Entity
          gltf-model="url(https://raw.githubusercontent.com/AnalyticalGraphicsInc/cesium/master/Apps/SampleData/models/GroundVehiclePBR/GroundVehiclePBR.gltf)"
          position={{x: 0, y: 0, z: -3}}
          />
        <Entity
          primitive="a-light"
          type="point"
          penumbra="1"
          intensity="0.6"
          position="-2.14 10.648 -3.237"
        />
      </Scene>
    );
  }

  render() {
    const { data } = this.state
    return (
      <div>
        <button onClick={this.start}>Start</button>
        <button onClick={this.stop}>Stop</button>
        {this.plotData()}
        {this.renderWebVR()}
      </div>
    );
  }
}

const root = document.getElementById('root')
render(<App />, root);
