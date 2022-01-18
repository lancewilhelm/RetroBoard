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
				<div className={styles.color} style={{background: `rgba(${ props.color.r }, ${ props.color.g }, ${ props.color.b }, ${ props.color.a })`}} />
			</div>
			{displayColorPicker ? (
				<div className={styles.popover} >
					<div className={styles.cover} onClick={handleClose} />
					<ChromePicker 
						color={props.color} 
						onChange={(color, event) => props.setColor(color)} 
						onChangeComplete={props.changeColor} 
						disableAlpha={true}
					/>
				</div>
			) : null}
		</div>
	);
}
