import React from 'react';
import './Results.css';
import '../../styles/colors.css'
import WellDescription from '../../components/WellDescription/WellDescription';
import WellComposition from '../../components/WellComposition/WellComposition';
import Map from '../../components/Map/Map';
import Svg from '../../components/Svg/Svg'

function Results({fileName}) {
    
    // const data2 = [
    //     { value: 10, label: 'apples', color: '#ffc800' }, 
    //     { value: 20, label: 'bananas', color: '#28c896' },
    //     { value: 30, label: 'oranges', color: '#96e600' },
    //     { value: 20, label: 'oranges', color: '#32c8c8' },
    //   ]

    return (
        <div className='results' id='results'> 
        <a href='#home'>
            <Svg></Svg>
        </a>
            <div className='results-main'>
            <div className='map_and_description'>
                <Map fileName={fileName}></Map>
                <WellDescription></WellDescription>
            </div>
            <WellComposition></WellComposition>
            </div>
           
        </div>
    );
}

export default Results;