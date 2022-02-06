import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/TickerSettings.module.css';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Autocomplete, Chip, TextField } from '@mui/material';
import { localIP } from './config';

export default function TickerSettings(props) {
	const [settings, setSettings] = useState({});
	const [scroll, setScroll] = useState('paper');
	const [tickerType, setTickerType] = useState();

	const typeList = ['stock', 'crypto'];

	function changeTickerType(e, val) {
		setTickerType(val);
	}

	function sendSettings() {
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(settings),
		};
		fetch('http://' + localIP + ':5000/api/settings', requestOptions);
		props.handleDialogClose();
	}

	useEffect(() => {
        fetch('http://' + localIP + ':5000/api/settings')
            .then((res) => res.json())
            .then((data) => {
                props.setSettings(data);
            });
    }, [props.resetSettings]);

	return (
		<div className={styles.container}>
			<Dialog
				open={props.tickerSettingsOpen}
				onClose={props.handleTickerSettingsClose}
				scroll={scroll}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
				className={styles.dialog}
			>
				<DialogTitle>Ticker Settings</DialogTitle>
				<DialogContent className={styles.settingsBody}>
					<div className={styles.settingsContainer}>
						<Autocomplete
							disablePortal
							className={styles.textBox}
							id='color-mode-selector'
							options={typeList}
							sx={{ width: 200 }}
							onChange={(e, val) => changeTickerType(e, val)}
							renderInput={(params) => (
								<TextField {...params} label='Type' />
							)}
						/>
						<Chip label={tickerType} variant='outlined' />
					</div>
				</DialogContent>
				<DialogActions>
					<Button
						className={styles.button}
						variant='outlined'
						color='error'
						onClick={() => props.setResetSettings(!props.setResetSettings)}
					>
						Reset
					</Button>
					<Button
						className={styles.button}
						variant='outlined'
						onClick={props.handleTickerSettingsClose}
					>
						Close
					</Button>
					<Button 
					className={styles.button}
					variant='outlined' 
					color='success'
					onClick={null}>
						Save Changes
					</Button>
				</DialogActions>
			</Dialog>
		</div>
	);
}
