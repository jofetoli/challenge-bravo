import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
      { duration: '2s', target: 3300 },
      { duration: '60s', target: 3300 },
      { duration: '2s', target: 0 },
    ],
  };

  export default function () {
    let res = http.get('http://localhost:5678/currency/convert?from=USD&to=BRL&amount=1');
    check(res, {
     'is status 200': (r) => r.status === 200,
   });
    sleep(0.1);
  }