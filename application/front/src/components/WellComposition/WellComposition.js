import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Pie3D } from 'react-pie3d'
import './WellComposition.css'

function WellComposition(props) {
    const[wellComposition, setWellComposition] = useState([]);
    useEffect(() => {
            axios.get('http://127.0.0.1:8000/api/get_well_composition/', {params : {file_name: '15_2-1__WELL__15-02-01_PB-706-0386.pdf'}})
            .then(function (response) {
                setWellComposition(response.data)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                //setLoading(false);
            });
    }, []);

 
  
    return (
        <div className="piechart">
            <Pie3D config={{size: 0.8, ir: 0, height: 60, angle: 60, strokeWidth:5}} data={wellComposition} />
        </div>
          
        );
}

export default WellComposition;