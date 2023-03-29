import React from 'react';
import { Icon } from '@iconify/react'
import locationIcon from '@iconify/icons-mdi/map-marker'

function LocationPin(props) {
    return (
    <div className="pin">
        <Icon icon={locationIcon} className="pin-icon" />
        <p className="pin-text">{"Yoooooo"}</p>
    </div>
    );
}

export default LocationPin;