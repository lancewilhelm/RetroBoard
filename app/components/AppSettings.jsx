import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/AppSettings.module.css';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Autocomplete, Chip, TextField, getRadioUtilityClass } from '@mui/material';
import { localIP } from './config';

export default function AppSettings(props) {
	const [scroll, setScroll] = useState('paper');
	const [appSettings, setAppSettings] = useState(null);

	function sendSettings(e) {
		e.preventDefault();
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(props.settings),
		};
		fetch('http://' + localIP + '/api/settings', requestOptions);
		props.handleAppSettingsClose();
	}

	function renderSettingsItems() {
		if (appSettings !== null) {
			let items = [];
			for (const setting in appSettings) {
				if (appSettings[setting].type === 'list') {
					items.push(
						<div className={styles.settingsContainer} key={setting}>
							<Autocomplete
								disablePortal
								className={styles.textBox}
								options={appSettings[setting].options}
								sx={{ width: 200 }}
								// onChange={(e, val) => changeGraphType(e, val)}
								renderInput={(params) => (
									<TextField {...params} label={setting} />
								)}
							/>
							<Chip label={appSettings[setting].value} variant='outlined' />
						</div>
					)
				} else if (appSettings[setting].type === 'field') {
					items.push(
						<div className={styles.settingsContainer} key={setting}>
							<TextField
								className={styles.textBox}
								sx={{ width: 200 }}
								label='Symbol'
								// onChange={(e) => changeSymbol(e)}
								/>
							<Chip label={appSettings[setting].value} variant='outlined' />
						</div>
					)
				}
			}
			return items;
		}
	}

	useEffect(() => {
		if (props.app !== null) {
			try {
				const s = require('../../api/apps/' + props.app.toLowerCase() + '.json');
				setAppSettings(s);
			} catch {
				setAppSettings(null);
			}
		};
	}, [props.app]);

	return (
		<div className={styles.container}>
			<Dialog
				open={props.appSettingsOpen}
				onClose={props.handleAppSettingsClose}
				scroll={scroll}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
				className={styles.dialog}
			>
				<DialogTitle>{props.app} Settings</DialogTitle>
				<form onSubmit={sendSettings}>
					<DialogContent className={styles.settingsBody} >
						{renderSettingsItems()}
					</DialogContent>
					<DialogActions>
						<Button
							className={styles.button}
							variant='outlined'
							color='error'
							type='button'
							onClick={() => props.setResetSettings(!props.resetSettings)}
						>
							Reset
						</Button>
						<Button
							className={styles.button}
							variant='outlined'
							type='button'
							onClick={props.handleAppSettingsClose}
						>
							Close
						</Button>
						<Button 
						className={styles.button}
						variant='outlined' 
						color='success'
						onClick={sendSettings}
						type='submit'
						autoFocus>
							Save Changes
						</Button>
					</DialogActions>
				</form>
			</Dialog>
		</div>
	);
}