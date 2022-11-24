import wx
import pandas as pd

namesList = {
    'Exercise': ['Air Bike', 'Treadmill'],
    'Clothing': ['Sweatshirt', 'Leggings'],
    'Yoga': ['Yoga Mat', 'Yoga Block'],
    'Boxing': ['Punching Bag', 'Pull Up Bar'],
    'Strength': ['Adjustable Dumbbell', 'Dip Station'],
    'Food': ['Whey Protein', 'Country Egg']
}

Cart = []
Total_Price=0

productsDf = pd.read_csv('assets/products.csv')

class MyFrame(wx.Frame):
    def OnTypeCombo(self, event):
        self.nameBox.Clear()
        for item in namesList[self.typeBox.GetValue()]:
            self.nameBox.Append(item)

    def onNameCombo(self, event):
        val = self.nameBox.GetValue()

        if val == '--Choose Fitness and Exercise Product Type--':
            return

        row = productsDf.loc[productsDf['name'] == val]
        row = row.to_dict(orient='records')[0]

        bmp = wx.Image('assets/{}'.format(row['image']), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = bmp.ConvertToImage()
        bmp = wx.Bitmap(image.Scale(100, 100))
        self.productImage.SetBitmap(bmp)

        self.productText.SetLabel('Name : ' + row['name'])
        self.productText.SetLabel('Brand : ' + row['brand'])
        self.priceText.SetLabel('Price : Rs. ' + str(row['price']))
        self.quantityText.SetLabel('Quantity : ' + str(row['quantity']))
        self.stockText.SetLabel('Stock : ' + str(row['stock']))

    def AddToCart(self, event):

        Product_name = self.nameBox.GetValue()
        Product_type = self.typeBox.GetValue()
        
        if Product_name == '--Choose Product Type--' or Product_name == '':
            wx.MessageBox("Please select atleast one item", "Warning")
            return

        else:

            if Product_name in Cart:
                wx.MessageBox(Product_name + " is already in the Cart", "Cart")
                return
            
            Cart.append(Product_name)
            wx.MessageBox(Product_name + " is added to Cart ","Success")
            
            print(Cart)


    def Display_Cart(self, event):

        if(len(Cart)==0):
            wx.MessageBox("Your cart is empty!", "Cart Details")
            return
        
        Products=""

        i=1
        for product in Cart:
            Products+=str(i) + ". " + product + "\n"
            i += 1

        wx.MessageBox(Products, "Cart Details")
           
        
    def __init__(self):
        super().__init__(parent = None, title = 'The Exercise and Fitness Store')

        opanel = wx.Panel(self)
        osizer = wx.BoxSizer(wx.VERTICAL)

        typeSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        typeText = wx.StaticText(opanel, label = 'Product Type : ')
        typesList = ['Exercise', 'Clothing', 'Yoga', 'Boxing', 'Strength', 'Food']
        self.typeBox = wx.ComboBox(opanel, choices = typesList)
        self.typeBox.Bind(wx.EVT_COMBOBOX, self.OnTypeCombo)
        
        typeSizer.Add(typeText, 3, wx.ALL | wx.EXPAND | wx.CENTER, border = 20)
        typeSizer.Add(self.typeBox, 5, wx.ALL | wx.EXPAND | wx.CENTER, border = 20)

        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        nameText = wx.StaticText(opanel, label = 'Product Name : ')
        namesList = ['--Choose Product Type--']
        
        self.nameBox = wx.ComboBox(opanel, choices = namesList)
        self.nameBox.Bind(wx.EVT_COMBOBOX, self.onNameCombo)
        
        nameSizer.Add(nameText, 3, wx.ALL | wx.EXPAND | wx.CENTER, border = 20)
        nameSizer.Add(self.nameBox, 5, wx.ALL | wx.EXPAND | wx.CENTER, border = 20)

        
        listSizer = wx.BoxSizer(wx.HORIZONTAL)

        bmp = wx.Image('assets/default.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = bmp.ConvertToImage()
        bmp = wx.Bitmap(image.Scale(100, 100))
        self.productImage = wx.StaticBitmap(opanel, -1, bmp, size = (100, 100))
        listSizer.Add(self.productImage, 4, wx.ALL | wx.EXPAND | wx.CENTER, border = 20)

        attrSizer = wx.BoxSizer(wx.VERTICAL)
        self.productText = wx.StaticText(opanel, label = '')
        attrSizer.Add(self.productText, 4, wx.ALL | wx.EXPAND | wx.CENTER, border = 10)
        self.priceText = wx.StaticText(opanel, label = '')
        attrSizer.Add(self.priceText, 4, wx.ALL | wx.EXPAND | wx.CENTER, border = 10)
        self.quantityText = wx.StaticText(opanel, label = '')
        attrSizer.Add(self.quantityText, 4, wx.ALL | wx.EXPAND | wx.CENTER, border = 10)
        self.stockText = wx.StaticText(opanel, label = '')
        attrSizer.Add(self.stockText, 4, wx.ALL | wx.EXPAND | wx.CENTER, border = 10)
        
        listSizer.Add(attrSizer)

        btnSizer= wx.BoxSizer(wx.HORIZONTAL)

        self.AddBtn = wx.Button(opanel,5,"Add to Cart")
        self.DisplayCart = wx.Button(opanel,6,"Display your cart")

        self.AddBtn.Bind(wx.EVT_BUTTON,self.AddToCart)
        self.DisplayCart.Bind(wx.EVT_BUTTON,self.Display_Cart)
        
        btnSizer.Add(btnSizer.AddSpacer(20))
        btnSizer.Add(self.AddBtn, 1, wx.CENTER)
        btnSizer.Add(btnSizer.AddSpacer(20))
        btnSizer.Add(self.DisplayCart, 1, wx.CENTER)
        
        osizer.Add(typeSizer)
        osizer.Add(typeSizer.AddStretchSpacer())
        osizer.Add(nameSizer)
        osizer.Add(typeSizer.AddStretchSpacer())
        osizer.Add(listSizer)
        osizer.Add(typeSizer.AddStretchSpacer())
        osizer.Add(btnSizer)
        osizer.Add(typeSizer.AddStretchSpacer())

        opanel.SetSizer(osizer)

        ico = wx.Icon('assets/grocery_bag.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.SetSize(self.MinSize)
        self.Centre()
        self.Show()

app = wx.App()
frame = MyFrame()
app.MainLoop()
