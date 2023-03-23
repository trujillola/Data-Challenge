import React from 'react';
import './Results.css';
import { Pie3D } from 'react-pie3d'
import '../../styles/colors.css'
function Results(props) {
    const data = [
        { value: 10, label: 'apples', color: '#ffc800' }, 
        { value: 20, label: 'bananas', color: '#28c896' },
        { value: 30, label: 'oranges', color: '#96e600' },
        { value: 20, label: 'oranges', color: '#32c8c8' },
      ]
    return (
        <div className='results' id='main'>
            <h1>coucou</h1>
            <Pie3D config={{size: 0.6, ir: 0, height: 80, angle: 60, strokeWidth:5}} data={data} />
        </div>
    );
}

export default Results;