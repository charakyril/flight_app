<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Results</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #b57c7c; padding: 8px; text-align: left; }
    th { background: #f0f0f0; }
    a { display: inline-block; margin-top: 16px; color: #2a4d69; }
  </style>
</head>
<body>
  <h1>Results</h1>
  % if rows:
    <table>
      <tbody>
        % for row in rows:
          <tr>
            % for cell in row:
              <td>{{cell}}</td>
            % end
          </tr>
        % end
      </tbody>
    </table>
  % else:
    <p>No results were returned by the query.</p>
  % end
  <a href="/">Back</a>
</body>
</html>
