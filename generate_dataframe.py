import pandas as pd
import numpy as np


def create_visualization(df, result_df, pair_index, current_row=None):
    """Creates a styled visualization of which cells are being averaged and subtracted"""

    def highlight_cells(x):
        df_highlighted = pd.DataFrame('', index=x.index, columns=x.columns)
        # Highlight the pair in row P
        col1, col2 = str(2*pair_index + 1), str(2*pair_index + 2)
        df_highlighted.loc['P', col1] = 'background-color: yellow'
        df_highlighted.loc['P', col2] = 'background-color: yellow'

        # If we're showing the subtraction process
        if current_row is not None:
            # Highlight the cells being processed
            df_highlighted.loc[current_row,
                               col1] = 'background-color: lightgreen'
            df_highlighted.loc[current_row,
                               col2] = 'background-color: lightgreen'

        return df_highlighted

    # Create a styled dataframe
    styled_df = df.style.apply(highlight_cells, axis=None)

    # Get the pair values and average
    col1, col2 = str(2*pair_index + 1), str(2*pair_index + 2)
    val1, val2 = df.loc['P', col1], df.loc['P', col2]
    avg = (val1 + val2) / 2

    # Create the HTML content
    html_content = f'''
    <h2>{"Subtraction " if current_row else ""}Step {pair_index + 1}: {"Row " + current_row + ": " if current_row else ""}Columns {col1} & {col2}</h2>
    '''

    if not current_row:
        html_content += f'<p>Values being averaged from row P: {
            val1} and {val2} = {avg}</p>'
    else:
        # Show the subtraction operation for the current cells
        orig_val1 = df.loc[current_row, col1]
        orig_val2 = df.loc[current_row, col2]
        new_val1 = result_df.loc[current_row, col1]
        new_val2 = result_df.loc[current_row, col2]
        html_content += f'''
        <p>Subtracting {avg} from cells in row {current_row}:</p>
        <p>Column {col1}: {orig_val1} - {avg} = {new_val1}</p>
        <p>Column {col2}: {orig_val2} - {avg} = {new_val2}</p>
        '''

    html_content += f'{styled_df.to_html()}<hr>'
    return html_content


def subtract_row_P_averages(df):
    """
    Subtracts the average of row P column pairs from all values in rows A-O.
    Column pairs are: (1,2), (3,4), (5,6), etc.
    """
    # Create a copy of the dataframe to avoid modifying the original
    result_df = df.copy()

    # Start HTML file
    html_output = '''
    <html>
    <body style="font-family: Arial, sans-serif;">
    <h1>Row P Column Pair Averaging Process</h1>
    <p style="color: #666;">
    Yellow highlights: Cells being averaged in row P<br>
    Green highlights: Cells being processed in the current row
    </p>
    '''

    # Only process first two pairs (columns 1-4)
    for i in range(2):  # Only process pairs 0 and 1
        # First show which cells are being averaged
        html_output += create_visualization(df, result_df, i)

        # Calculate the average for this pair
        col1 = str(2*i + 1)
        col2 = str(2*i + 2)
        row_P = df.loc['P']
        pair_avg = (row_P[col1] + row_P[col2]) / 2

        # Show the subtraction process for each row A-O
        for row in df.index[:-1]:  # All rows except P
            # Subtract the average
            result_df.loc[row, col1] -= pair_avg
            result_df.loc[row, col2] -= pair_avg

            # Show the visualization for this step
            html_output += create_visualization(df, result_df, i, row)

    # Close HTML file
    html_output += '</body></html>'

    # Save the visualization
    with open('averaging_process.html', 'w') as f:
        f.write(html_output)

    # Continue processing the remaining columns without visualization
    for i in range(2, 12):  # Process remaining pairs
        col1 = str(2*i + 1)
        col2 = str(2*i + 2)
        pair_avg = (row_P[col1] + row_P[col2]) / 2
        for row in df.index[:-1]:
            result_df.loc[row, col1] -= pair_avg
            result_df.loc[row, col2] -= pair_avg

    return result_df


# Create row and column labels
row_labels = [chr(i) for i in range(65, 65+16)]  # A through P
col_labels = [str(i) for i in range(1, 25)]      # 1 through 24

# Generate random data for the dataframe
# 11 because randint upper bound is exclusive
data = np.random.randint(1, 11, size=(16, 24))

# Create the dataframe with labels
df = pd.DataFrame(data, index=row_labels, columns=col_labels)
df = df.astype(float)  # Convert to float type to handle decimal values

# Apply the subtraction function
result_df = subtract_row_P_averages(df)

# Save both original and processed dataframes to CSV
df.to_csv('original_dataframe.csv')
result_df.to_csv('processed_dataframe.csv')

print("Original DataFrame has been saved to 'original_dataframe.csv'")
print("Processed DataFrame has been saved to 'processed_dataframe.csv'")
print("Visualization of the averaging process has been saved to 'averaging_process.html'")
