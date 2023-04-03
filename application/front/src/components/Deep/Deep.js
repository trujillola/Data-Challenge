import React, { useState, useEffect } from 'react';
import './Deep.css'
import axios from 'axios';

function Deep(props) {
    const[min, setMin] = useState('');
    const[max, setMax] = useState('');
    const[isClick, setIsCLick] = useState(false)
    function handleChangeMin(event) {
        const min = event.target.value;
        setMin(min);
        setIsCLick(false);
      }

      function handleChangeMax(event) {
        const max = event.target.value;
        setMax(max);
        setIsCLick(false);
      }

      function handleClick(event) {
        setIsCLick(true);
      }

      useEffect(() => {
        if (isClick) {
            axios.post('http://127.0.0.1:8000/api/crop_image_deep/?min='+min+'&max='+max)
            .then(function (response) {
                //setWellDescription(response.data)
                console.log(response.data)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                //setLoading(false);
            });
        }
    }, [isClick]);
    return (
        <div className='btn-deep'>
            <p>If you want to crop the image depending of the deep please enter the min and max deep.</p>
            <div className='ctn-btn-min-max'>
                <label className='label-number'>
                    Enter min :
                    <input type='number' min={0} className='btn-input-number' placeholder="000"  value={min} onChange={handleChangeMin}></input>
                </label>
                <label className='label-number'>
                    Enter max :
                    <input type='number' className='btn-input-number' placeholder="999"  value={max} onChange={handleChangeMax}></input>
                </label>
                <button className='btn-crop-img' onClick={handleClick}>Crop image</button>
            </div>
            
        </div>
    );
}

export default Deep;