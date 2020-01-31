<?php

function getClientMac($clientIP)
{
    return trim(exec("grep " . escapeshellarg($clientIP) . " /tmp/dhcp.leases | awk '{print $2}'"));
}

function getClientSSID($clientIP)
{
    $mac = getClientMac($clientIP);

    $pineAPLogPath = trim(file_get_contents('/etc/pineapple/pineap_log_location'));

    return trim(exec("grep " . $mac . " " . $pineAPLogPath . "pineap.log | grep 'Association' | awk -F ',' '{print $4}'"));

}
function getClientHostName($clientIP)
{
    return trim(exec("grep " . escapeshellarg($clientIP) . " /tmp/dhcp.leases | awk '{print $4}'"));
}