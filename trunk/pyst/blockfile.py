__author__ = 'are'


class BlockFile:

    class FileBlock:
        name = ""
        content = []

        def __init__(self, name=""):
            self.name = name
            self.content = []

    fileHeader = []
    fileBlocks = []
    fileBlocksDict = {}

    def _loadblocks(self, lines):
        self.fileHeader = []
        self.fileBlocks = []
        bname = "__header__"
        for line in lines:
            if line[0] == "*":
                bname = line.strip("*").strip()
                self.fileBlocks.append(self.FileBlock(bname))  # add a new block
                continue

            if bname == "__header__":
                #add the line to the fileHeader
                self.fileHeader.append(line.strip())
            else:
                #add the line to the content of the last (current) block
                self.fileBlocks[-1].content.append(line.strip())

    def _createBlockDict(self):
        self.fileBlocksDict = {}

        for block in self.fileBlocks:
            if block.name in self.fileBlocksDict == "multiple instances!":
                continue

            if block.name in self.fileBlocksDict:
                self.fileBlocksDict[block.name] = "multiple instances!"
            else:
                self.fileBlocksDict[block.name] = block

    def __init__(self,filename):
        bfile = open(filename)
        lines = bfile.readlines()
        bfile.close()
        self._loadblocks(lines)
        self._createBlockDict()
