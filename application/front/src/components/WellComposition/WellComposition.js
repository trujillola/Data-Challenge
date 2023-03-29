import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Pie3D } from 'react-pie3d'
import './WellComposition.css'
import Loading from '../Loading/Loading'

function WellComposition({fileName, startScrapping}) {
    const[wellComposition, setWellComposition] = useState([]);
    const[loading, setLoading] = useState(true)
    useEffect(() => {
        if(startScrapping){
            axios.get('http://127.0.0.1:8000/api/get_well_composition/', {params : {file_name: fileName}})
            .then(function (response) {
                setWellComposition(response.data)
                console.log("well composition = ", wellComposition)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                setLoading(false);
            });
        }
    }, [startScrapping]);

    // const [dict_composition, setDictComposition] = useState([{ 'value': 93.35, 'label': 'sand', 'color': '#ffc800' }, 
    //     { 'value': 18.35, 'label': 'sand_clay', 'color': '#28c896'  }])
    //      //{ 'value': 90, 'label': 'stone', 'color': '#96e600'  }]
  
    return (
        <div className="piechart">
            {loading? 
            <Loading></Loading> :
            <Pie3D config={{size: 1.1, ir: 0, height: 60, angle: 60, strokeWidth:5}} data={wellComposition} />
            }
        </div>
          
        );
}

export default WellComposition;