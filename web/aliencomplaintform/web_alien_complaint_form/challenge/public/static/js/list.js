const display = feedback => {
    document.getElementsByTagName('tbody')[0].innerHTML = '';
    for(let complaint of feedback) {
        let template = `
            <tr>
                <th scope="row">${complaint.id}</th>
                <td>${complaint.complaint}</td>
                <td>${complaint.species}</td>
                <td>${complaint.created_at}</td>
            </tr>
        `;
        
        document.getElementsByTagName('tbody')[0].innerHTML += template;
    }
};

const jsonp = (url, callback) => {
    const s = document.createElement('script');

    if (callback) {
        s.src = `${url}?callback=${callback}`;
    } else {
        s.src = url;
    }

    document.body.appendChild(s);
};

jsonp('/api/jsonp', (new URLSearchParams(location.search)).get('callback'));