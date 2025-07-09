## UX Mockups
This is a prose for the mockup of the mobile for member persona.
A single page mobile app that shows 



 app that can display table with following columns:
- View Receipt, Merchant, Address, County, Date, Total, Tax
sorted by Date
where View Receipt is an icon when clicked should expand the row Hight and show the receipt image with the rest of the info on the sided.  When clicked again should colapse the row to original view.

Data in the table should be synced from an MCP Google Drive Server for a given folder where images are stored.  The MCP server is like this one https://github.com/felores/gdrive-mcp-server
If needed the data sync should happen everytime app is loaded or on demand when Sync button at the top right corner is pressed.

At he the top of the page above the receipts table there should be a search bar to perform a vector search for all columns except date.

At the bottom right of the page there should be an Export button.  When clicked it should export table contents to a new Google spreadsheet using an MCP server like that https://github.com/xing5/mcp-google-sheets.