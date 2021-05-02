import { Button } from 'react-bootstrap';
import styles from '../styles/Main.module.css';

export default function Main() {
    function sendCommand(command) {
        const url_base = 'http://localhost:5000/api/';

        const res = fetch(url_base + command, {
            method: 'GET',
        });
        return;
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
