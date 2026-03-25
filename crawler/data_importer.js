function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function playstation() {
    const gameInfo = require('./raw_data/playstation_gameInfo.json');
    for (let item = 0; item < gameInfo.length; item++) {
        await sleep(1000);
        console.log(item + '/' + gameInfo.length);
        let date = gameInfo[item].date.split('/');
        date = date[2] + '-' + date[1] + '-' + date[0]

        var formdata = new FormData();
        formdata.append("game_name", gameInfo[item].name.trim());
        formdata.append("game_img", gameInfo[item].img);
        formdata.append("game_url", gameInfo[item].url);
        formdata.append("game_rating", parseFloat(gameInfo[item].rating.trim()));
        formdata.append("game_price", gameInfo[item].price.replace('NT$', '').replace(',', '').trim());
        formdata.append("platform", gameInfo[item].platform.map(list => list.trim()));
        formdata.append("game_date", date);
        formdata.append("game_publisher", gameInfo[item].publisher.trim());
        formdata.append("category", gameInfo[item].category.map(list => list.trim()));

        // console.log(formdata)
        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow',
        };

        fetch("http://127.0.0.1:8000/api/gameprofile/profilePost/", requestOptions)
            .then(response => {
                if (response.ok) {
                    console.log('ok')
                }
            });
    }
}

async function nintendo() {
    const gameInfo = require('./raw_data/nintendo_gameInfo.json');
    for (let item = 0; item < gameInfo.length; item++) {
        await sleep(1000);
        console.log(item + '/' + gameInfo.length);
        let date = gameInfo[item].date.split('/');
        date = date[0] + '-' + date[1] + '-' + date[2]

        var formdata = new FormData();
        formdata.append("game_name", gameInfo[item].name.trim());
        formdata.append("game_img", gameInfo[item].img);
        formdata.append("game_url", gameInfo[item].url);
        formdata.append("game_rating", parseFloat(gameInfo[item].rating));
        formdata.append("game_price", gameInfo[item].price);
        formdata.append("platform", gameInfo[item].platform.map(list => list.trim()));
        formdata.append("game_date", date);
        formdata.append("game_publisher", gameInfo[item].publisher.trim());
        formdata.append("category", gameInfo[item].category.map(list => list.trim()));

        // console.log(formdata)
        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow',
        };

        fetch("http://127.0.0.1:8000/api/gameprofile/profilePost/", requestOptions)
            .then(response => {
                if (response.ok) {
                    console.log('ok')
                }
            });
    }
}

nintendo()