import { Button } from 'react-bootstrap';
import styles from '../styles/Main.module.css';
import { localIP } from './config';

//! You must set your local IP address below so that the
export default function Main() {
    async function sendCommand(command) {
        const url_base = 'http://' + localIP + ':5000/api/';

        const res = await fetch(url_base + command, {
            method: 'GET',
        });
        return res;
    }

    return (
        <div className={styles.container}>
            <Button
                variant='outline-dark'
                onClick={() => sendCommand('rotate')}
            >
                Rotating Square
            </Button>
        </div>
    );
}
