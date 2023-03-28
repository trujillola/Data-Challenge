import React, { useEffect, useState } from 'react';
import features from './features.json'
import './Map.css'
import {
    ComposableMap,
    Geographies,
    Geography,
    Marker,
    ZoomableGroup
  } from "react-simple-maps";
import axios from 'axios';

function Map({fileName}) {
    const color = [ "#ff0000", "#ffc800", "#96e600", "#28c896", "#32c8c8", "#009bff", "#285aff"];
    const [wellPosition, setWellPosition] = useState({name : 'Pau', coordinates: [-0.370797, 43.2951] })
    console.log("filename = ", fileName)
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get_well_position/', {params : {file_name: fileName}})
        .then(function (response) {
            setWellPosition(response.data)
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(() => {
            console.log('finally')
            //setLoading(false);
        });
}, []);

    const markers = [
    {
        markerOffset: -30,
        name: wellPosition.name,
        coordinates: wellPosition.coordinates
    }
    ];

   
    return (
        <ComposableMap
        projection="geoMercator"
        projectionConfig={{
            center: wellPosition.coordinates,
            scale: 400
        }}
      >
        <ZoomableGroup center={wellPosition.coordinates} zoom={1}>
        <Geographies geography={features}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography 
                key={geo.rsmKey}
                geography={geo}
                fill="#FFFFFF"
                stroke="#FFFFFF"
                style={{
                    default: {
                      fill: "#CACFD2",
                    },
                    hover: {
                      fill: color[Math.floor(Math.random() * 6)], 
                    },
                    pressed: {
                      fill: "none",
                    },
                  }}
              />
            ))
          }
        </Geographies>
        {markers.map(({ name, coordinates, markerOffset }) => (
        <Marker key={name} coordinates={coordinates}>
          <g
            fill="none"
            stroke="#ff0000"
            strokeWidth="5"
            strokeLinecap="round"
            strokeLinejoin="round"
            transform="translate(-12, -24)"
          >
            <circle cx="12" cy="10" r="3" />
            <path style={{
                fill: "#FFFFFF"
              }} d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 6.9 8 11.7z" />
          </g>
          <text
            textAnchor="middle"
            y={markerOffset}
            style={{ fontFamily: "system-ui", fill: "#ff0000", fontSize: "18px" }}
          >
            {name}
          </text>
        </Marker>
      ))}
      </ZoomableGroup>
      </ComposableMap>
    );
  
}

export default Map;