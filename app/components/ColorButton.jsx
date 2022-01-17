import React from 'react';
import { ChromePicker } from 'react-color';
import { useState } from 'react';
import styles from '../styles/ColorButton.module.css'

export default function ColorButton(props) {
	const [displayColorPicker, setDisplayColorPicker] = useState(false);

    function handleClick() {
		setDisplayColorPicker(true)
    };

    function handleClose() {
        setDisplayColorPicker(false)
    };

	return (
		<div className={styles.container}>
			<div className={styles.swatch} onClick={handleClick}>
				<div className={styles.color} style={{background: `rgba(${ props.staticColor.r }, ${ props.staticColor.g }, ${ props.staticColor.b }, ${ props.staticColor.a })`}} />
			</div>
			{displayColorPicker ? (
				<div className={styles.popover} >
					<div className={styles.cover} onClick={handleClose} />
					<ChromePicker 
						color={props.staticColor} 
						onChange={(color, event) => props.setStaticColor(color)} 
						onChangeComplete={props.changeStaticColor} 
						disableAlpha={true}
					/>
				</div>
			) : null}
		</div>
	);
}
