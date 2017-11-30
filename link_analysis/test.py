from flask import Flask, render_template, request
import sys
import json
import requests
import network











def main():
    outlinks = ["www.example.com","www.example2.com","www.example3.com"]
    test_network = network.Network()
    test_network.prioritizer(outlinks)



main()
