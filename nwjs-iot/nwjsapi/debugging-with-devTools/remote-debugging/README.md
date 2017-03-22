Purpose: Use the --remote-debugging-port=port command line option to specify which port the DevTools should listen to
Test Steps:
           1.Execute command 'nw --remote-debugging-port=9222 .' under current path.
           2.Open http://localhost:9222/ in your browser to visit the debugger remotely.
           3.Test passes if Debugging Tools is opened.
