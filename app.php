<?php
$token = "6752828920:AAE2gg3Mb2dftJ2vYaOcO6EXec-KHSfcFTA";
$link = "https://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

file_get_contents("https://api.telegram.org/bot$token/setwebhook?url=$link");

define('API_KEY', $token);

function bot($method, $datas = [])
{
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    } else {
        return json_decode($res);
    }
}

$update = json_decode(file_get_contents('php://input'));
$message = $update->message;
$forid = $message->forward_from_chat->id;
$message_id = $message->message_id;
$text = $message->text;
$name = $message->chat->first_name;
$cid = $message->chat->id;
$fid = $message->from->id;
$data = $update->callback_query->data;
$ccid = $update->callback_query->message->chat->id;
$cmid = $update->callback_query->message->message_id;

mkdir("data");
mkdir("data/$fid", 0777, true);
$step = file_get_contents("data/$fid/step.txt");
$baldir = "data/$fid/bal.dat";
$bal = file_get_contents($baldir);
$refcost = 0.001;

function sendm($id, $msg)
{
    $method = 'sendMessage';
    $datas = ([
        'chat_id' => $id,
        'text' => "*$msg*",
        "parse_mode" => "markdown"
    ]);
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    } else {
        return json_decode($res);
    }
}

function sendp($id, $photo)
{
    $method = 'sendPhoto';
    $datas = ([
        'chat_id' => $id,
        'photo' => "$photo",
        "parse_mode" => "markdown"
    ]);
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    } else {
        return json_decode($res);
    }
}

function delm($id, $mid)
{
    bot("DeleteMessage", [
        "chat_id" => $id,
        "message_id" => $mid,
    ]);
}

function sendpc($id, $photo, $caption)
{
    $method = 'sendPhoto';
    $datas = ([
        'chat_id' => $id,
        'photo' => "$photo",
        'caption' => $caption,
        "parse_mode" => "markdown"
    ]);
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    } else {
        return json_decode($res);
    }
}

function sendkeyboard($id, $message, $keyboard)
{
    bot('sendMessage', [
        'chat_id' => $id,
        'text' => $message,
        'reply_markup' => json_encode(['keyboard' => $keyboard, 'one_time_keyboard' => true, "resize_keyboard" => true]),
        "parse_mode" => "markdown",
    ]);
}

function setstep($id, $str)
{
    file_put_contents("data/$id/step.txt", $str);
}

function delstep($id)
{
    unlink("data/$id/step.txt");
}

function getstep($id)
{
    return file_get_contents("data/$id/step.txt");
}

function setbal0($id)
{
    file_put_contents("data/$id/bal.dat", "0");
}

function setval($id, $val, $value)
{
    file_put_contents("data/$id/$val.dat", $value);
}

function getval($id, $val)
{
    return file_get_contents("data/$id/$val.dat");
}

function getbal($id)
{
    return file_get_contents("data/$id/bal.dat");
}

function addbal($id, $deger)
{
    file_put_contents("data/$id/bal.dat", intval(file_get_contents("data/$id/bal.dat")) + $deger);
} 
?>
