%#template to generate an HTML form for a list of field names
<head>
    <style>
        label span {
            display: inline-block;
            width : 120px;
            text-align: right;
        }
        input {
            width: 100px;
            box-sizing: border-box;
            border: 1px solid #999;
        }
        button span {
            float: right;
        }
        p {
            margin: 2px;
        }
    </style>
</head>
<body>
<p>Add a new bike:</p>
<form action="/add_bike" method="post">
    <input type="hidden" name="type" value="{{geometry_type}}"/>
%for item in fields:
    %big_name = item.replace("_"," ").capitalize()
    <p>
    <label for="{{item}}">
        <span>{{big_name}}:</span>
    </label>
    <input id="{{item}}" type="number" step="any" min=0 name="{{item}}">
    </p>
%end
    <p>
        <span>
            <button type="submit">Save</button>
            <button>Cancel</button>
        </span>

    </p>
</form>
</body>
