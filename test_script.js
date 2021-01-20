import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
      { duration: '10s', target: 1000 },
      { duration: '10s', target: 2000 },
      { duration: '10s', target: 3000 },
    ],
  };

  export default function () {
    let res = http.get('http://localhost:8080/convert?from=USD&to=BRL&amount=1');
    check(res, {
     'is status 200': (r) => r.status === 200,
   });
    sleep(0.1);
  }