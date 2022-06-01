# Created by ezarourx at 1/26/2020
Feature: Trace IT E2E Full journey Tests
  # Enter feature description here

  Scenario: 1.Search text in "all" types filter search results,validate table, sort ,filter and export to CSV
    When user Choose All Category by DropDown
    And user Typing: ice lake p in the search TextField
    Then validate Search Results rising with categories
    When user click on search icon button
    Then validate Search Results found results in:All Categories
    When user checked checkbox:Lira category to filter
    Then validate Search Results found:60 results in:1 Categories
    When user unchecked checkbox:Lira category to filter
    And user checked checkbox:Die category to filter
    And user select and click on search result item with product_name:Ice Lake PCH-LP Die
    Then validate details page opens and contains the product id:10019672 and product name:Ice Lake PCH-LP Die and product_category:Die in the title
#    Then Validate Last Update by API in Details page DE82327
    When user Typing: 955800 in the Search & Filter TextField
    And user click on Export button
    Then validate UI with File from export
    When user click to sort column:Si Product Id
    Then validate column:Si Product Id sorted


  Scenario: 2nd journey (Quick Search)
    When user Choose All Category by DropDown
    And user Typing: Ice Lake in the search TextField
    Then validate Search Results rising with categories
    When user select suggest search Dropbox index: 0
    Then validate details page opens and contains the selected product info

      Scenario Outline: Flow 3.1 - Search by specific category without Category CATTS
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    Then validate Search Results rising with categories
    When user click on search icon button
    Then Validate categories filter not presented on Result page
    When user select and click on search result item with product_id:<selected_item>
    Then validate details page opens and contains the selected product info
    Examples:
      |search_category|search_text|selected_item|
      |IP Configuration|ice lake pgfx|93883|

  Scenario Outline: Flow 3.1 - Search by specific category without Category CATTS
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    Then validate Search Results rising with categories
    When user click on search icon button
    Then Validate categories filter not presented on Result page
    When user select and click on search result item with product_id:<selected_item>
    Then validate details page opens and contains the selected product info
    Examples:
      |search_category|search_text|selected_item|
      |IP Configuration|ice lake pgfx|93883|
#      |Board|ice lake-msft x|k58267-001|
#      |CPUID|CFL|0000906ebh|
#      |Die|Comet Lake|10041091|
#      |Finished Good|i5-8400 processor (9m cache, up to 4.00 ghz)|960619|
#      |IP Generation|csme 4.5|2217|
#      |Lira|ice lake u 4+2 2c 2g|10036095|
#      |Platform Config|coffee lake x|10033643|
#      |SW Ingredient|1407698538|1407698538|
#      |SW Kit|icl-u42-rs3-2018|1406873219|
#      |Si Product|alder lake p|10033908|

  Scenario Outline: Flow 3.2 - Search by Category CATTS
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    And user click on search icon button
    Then validate details page opens and contains the selected product info
    Then user switch between tabs and validate the table in each tab with API data by: category
    Examples:
      |search_category|search_text|
      |Visual ID|788D7X7904424|
      |Lot|L505B850|


#  Scenario: Flow 4- data validation
#    When user Choose All Category by DropDown
#    And user Typing: CML in the search TextField
#    Then validate Search Results rising with categories
#    When user click on search icon button
#    Then validate Search Results found results in:All Categories
#    When user checked checkbox:CPUID category to filter
#    Then validate Search Results found:8 results in:1 Categories
#    When user select and click on search result item with product_id:0000a0661h
#    Then validate details page opens and contains the product id:0000a0661h and product name:CML_K0 SysDebug patchID 0x800000DE and product_category:CPUID in the title
#    Then validate product all tabs names by API call in Details page
##    And user switch between tabs and validate the table in each tab with API data by: tab_index
#    Then user go back and selects a product from each category and validate the results in each tab
#    |text to search|checked|category        |results number|Item Code |product_name|
#    |-EV-          |checked|Board           |90            |k58267-001|ICE LAKE-MSFT X-EV-DVLP SY|
#    |Comet Lake    |checked|Die             |11            |10041091  |Comet Lake U/Y 4+2 With DDR4/LP3 Die|
#    |SR3QT         |checked|Finished Good   |6             |960619    |Intel® Core™ i5-8400 Processor (9M Cache, up to 4.00 GHz) FC-LGA14C, Tray|
#    |Ice lake pgfx |checked|IP Configuration|6             |93883     |Ice lake pGfx U 4+2 Windows Graphics Driver|
#    |Ice Lake U    |checked|Lira            |78            |10036095  |Ice Lake U 4+2 2C 2G M 17W superSKU|
#    |Coffee Lake X |checked|Platform Config |3             |10033643  |Coffee Lake X 4+0 (KBL CPU) Platform Configuration (Glacier Falls)|
#    |Ice Lake.sw.firmware.CSME|checked|SW Ingredient       |66         |1407698538|CSME  |
#    |BSF-HEDT-RST-Win10-2017WW3       |checked|SW Kit      |6          |1407288924|BSF-HEDT-RST-Win10-2017WW36.1.366|
#    |Comet Lake Y  |checked|Si Product      |2             |10041884   |Comet Lake Y 4+2 WITH DDR4/LP4X|
#    |csme          |checked|IP Generation   |33            |2217      |CSME 4.5.2|
#    When user go back and Search for:Ice Lake 10
#    Then validate that No results found in Search Result Page


  Scenario Outline: Flow 5.1 - View Results as a table
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    Then validate Search Results rising with categories
    When user click View All Results
    Then validate Search Results found results in equal to Home Page results
    When user iterate over results and count rows in each tab
    And user click Show Results as a Table
    Then validate details page title
    And validate number of rows in Details Page with number of rows from all results
    Examples:
      |search_category|search_text|
      |Lira|ice lake u 4+2 2c 1g 8|
#      |Board|ice lake dm|
#      |CPUID|Banias A-1|
#      |Die|10041872|
#      |Finished Good|960008|
#      |IP Configuration|ice lake pgfx s 4|
#      |IP Generation|csme 4.5.2|
#      |Platform Config|coffee lake x 6|
#      |SW Ingredient|1407698538| DE75282
#      |SW Kit|icl-u42-rs3-2018ww09|
#      |Si Product|alder lake pch-s r|

  Scenario Outline: Flow 5.2 -Negative- View Results as a table
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    Then validate Search Results rising with categories
    When user click View All Results
    Then validate Search Results found results in equal to Home Page results
    When user click Show Results as a Table
    Then validate error message on results page: Please refine your search to maximum of 5000 results
#    When user navigate by url to details page with term:<search_text> and category:<search_category>
#    Then validate error message on details page contains: Allowed: 5000 items
    Examples:
      |search_category|search_text|
      |Board|lake|

  Scenario Outline: Flow 5.3 -Negative- View Results as a table - Too much data 50,000
    When user Choose <search_category> Category by DropDown
    And user Typing: <search_text> in the search TextField
    Then validate Search Results rising with categories
    When user click View All Results
    Then validate Search Results found results in equal to Home Page results
#    Bug
#    When user click Show Results as a Table
#    And user switch to tab:2
#    Then validate error message on details page contains: Allowed: 50000 rows
    Examples:
      |search_category|search_text|
      |Finished Good|ice|